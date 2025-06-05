from fastapi import WebSocket, WebSocketDisconnect
from typing import List
import pika
import json
import xml.etree.ElementTree as ET
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from jose import JWTError, jwt
from pymongo import MongoClient
from datetime import datetime, timedelta
from bson import ObjectId
from jsonschema import validate, ValidationError
import os

# ========================
# CONFIGURAÇÕES GERAIS
# ========================

SECRET_KEY = "supersegredo123"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

MONGO_URL = os.getenv("MONGO_URL", "mongodb://mongo:27017")  # <- mongo container name
client = MongoClient(MONGO_URL)
db = client["biblioteca"]
livros_col = db["livros"]

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# ========================
# USUÁRIOS FAKE (DEMO)
# ========================

fake_users_db = {
    "admin": {"username": "admin", "password": "admin", "role": "admin"},
    "user": {"username": "user", "password": "user", "role": "user"}
}

# ========================
# APP FASTAPI
# ========================

app = FastAPI()

# Middleware CORS — necessário para funcionar com cliente em navegador
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Pode ajustar para ["http://localhost:8080"] se servir via http.server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# ========================
# WEBSOCKET - Notificações
# ========================

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()


# ========================
# JWT - Autenticação
# ========================

def create_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username not in fake_users_db:
            raise credentials_exception
        return fake_users_db[username]
    except JWTError:
        raise credentials_exception

@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = fake_users_db.get(form_data.username)
    if not user or user["password"] != form_data.password:
        raise HTTPException(status_code=400, detail="Credenciais inválidas")
    token = create_token({"sub": user["username"], "role": user["role"]})
    return {"access_token": token, "token_type": "bearer"}

# ========================
# JSON Schema para validação
# ========================

livro_schema = {
    "type": "object",
    "properties": {
        "titulo": {"type": "string"},
        "autor": {"type": "string"}
    },
    "required": ["titulo", "autor"]
}

# ========================
# RabbitMQ - envio de evento
# ========================

def enviar_evento(evento: dict):
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq"))
        channel = connection.channel()
        channel.queue_declare(queue="eventos")
        channel.basic_publish(exchange="", routing_key="eventos", body=str(evento))
        connection.close()
    except Exception as e:
        print("Erro ao enviar evento:", e)

# ========================
# CRUD de Livros
# ========================

@app.get("/livros", dependencies=[Depends(decode_token)])
def listar_livros():
    livros = list(livros_col.find({}, {"_id": 0}))
    return livros

@app.post("/livros")
async def criar_livro(livro: dict, user=Depends(decode_token)):
    try:
        validate(instance=livro, schema=livro_schema)
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=f"Erro de validação: {e.message}")
    
    livros_col.insert_one(livro)
    
    # Envia evento para RabbitMQ (já existente)
    enviar_evento({"evento": "livro_criado", "livro": livro, "user": user["username"]})
    
    # 🔔 Envia notificação por WebSocket
    await manager.broadcast(f"📚 Livro criado: {livro['titulo']} por {livro['autor']}")
    
    return {"msg": "Livro criado com sucesso"}


@app.delete("/livros/{titulo}", dependencies=[Depends(decode_token)])
def remover_livro(titulo: str):
    result = livros_col.delete_one({"titulo": titulo})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    return {"msg": "Livro removido"}

@app.get("/livros/protegido")
def endpoint_protegido(user=Depends(decode_token)):
    return {"msg": f"Bem-vindo {user['username']} com role {user['role']}"}

# ========================
# Exportação / Importação JSON e XML
# ========================

@app.get("/exportar/json")
def exportar_json():
    livros = list(livros_col.find({}, {"_id": 0}))
    with open("livros_export.json", "w") as f:
        json.dump(livros, f)
    return FileResponse("livros_export.json", media_type="application/json", filename="livros.json")

@app.post("/importar/json")
def importar_json():
    try:
        with open("livros_export.json", "r") as f:
            livros = json.load(f)
            for livro in livros:
                validate(instance=livro, schema=livro_schema)
                livros_col.insert_one(livro)
        return {"msg": "Importação JSON concluída"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao importar JSON: {str(e)}")

@app.get("/exportar/xml")
def exportar_xml():
    livros = list(livros_col.find({}, {"_id": 0}))
    root = ET.Element("livros")
    for l in livros:
        livro_elem = ET.SubElement(root, "livro")
        ET.SubElement(livro_elem, "titulo").text = l["titulo"]
        ET.SubElement(livro_elem, "autor").text = l["autor"]
    tree = ET.ElementTree(root)
    tree.write("livros_export.xml")
    return FileResponse("livros_export.xml", media_type="application/xml", filename="livros.xml")

@app.post("/importar/xml")
def importar_xml():
    try:
        tree = ET.parse("livros_export.xml")
        root = tree.getroot()
        for l in root.findall("livro"):
            titulo = l.find("titulo").text
            autor = l.find("autor").text
            livro = {"titulo": titulo, "autor": autor}
            validate(instance=livro, schema=livro_schema)
            livros_col.insert_one(livro)
        return {"msg": "Importação XML concluída"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao importar XML: {str(e)}")
    
# ========================
# WebSocket - Notificações em tempo real
# ========================

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()  # Mantém a conexão viva
    except WebSocketDisconnect:
        manager.disconnect(websocket)







