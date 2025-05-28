# 📚 Projeto Biblioteca - Integração de Sistemas

Este projeto demonstra um sistema distribuído de gestão de livros, integrando múltiplas tecnologias de serviços web.

---

## ✅ Tecnologias Implementadas

- **REST (FastAPI)** – CRUD + Autenticação OAuth2/JWT + MongoDB
- **GraphQL (Node.js + Apollo Server)** – Queries e mutations
- **SOAP (Node.js + node-soap)** – Operações XML com WSDL e XSD
- **gRPC (Python)** – Serviços unários e streaming com `.proto`
- **WebSockets (Python)** – Notificações em tempo real
- **RabbitMQ** – Comunicação assíncrona de eventos (ex: livro criado)
- **MongoDB** – Armazenamento NoSQL de livros
- **Docker** – Orquestração com Docker Compose
- **Cliente Python (CLI)** – Interage com todos os serviços

---

## 🧱 Arquitetura

Cliente Python CLI
↓ ↑
+--------------+ +------------------+ +------------------+
| WebSocket | ←──────→ | REST + MongoDB | ←─────→ | RabbitMQ |
| Notificações | | + Auth JWT | | (eventos/logs) |
+--------------+ +------------------+ +------------------+
↓
+-------------+ +----------------+
| GraphQL | | gRPC |
+-------------+ +----------------+
↓
+------------+
| SOAP |
+------------+


---

## ▶️ Como Executar (Docker)

### 🐳 Pré-requisitos:
- Docker
- Docker Compose

### Passos:
```bash
git clone <repo>
cd <repo>
docker-compose up --build

 Autenticação (OAuth2 + JWT)
POST /token
bash
Copiar
Editar
POST /token
Content-Type: application/x-www-form-urlencoded

username=admin&password=admin

Retorna:

json
Copiar
Editar
{
  "access_token": "<JWT>",
  "token_type": "bearer"
}
Usa o token com:

makefile
Copiar
Editar
Authorization: Bearer <token>
📘 Exemplos REST (http://localhost:5000)
GET /livros
bash
Copiar
Editar
curl -H "Authorization: Bearer <token>" http://localhost:5000/livros
POST /livros
bash
Copiar
Editar
curl -X POST http://localhost:5000/livros \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"titulo": "1984", "autor": "George Orwell"}'
DELETE /livros/{titulo}
bash
Copiar
Editar
curl -X DELETE http://localhost:5000/livros/1984 \
  -H "Authorization: Bearer <token>"
🔗 Endpoints de Outros Serviços
Serviço	URL Local
GraphQL	http://localhost:4000/graphql
SOAP WSDL	http://localhost:8000/wsdl?wsdl
gRPC	localhost:50051
WebSocket	ws://localhost:8765
RabbitMQ UI	http://localhost:15672
MongoDB	mongodb://localhost:27017

📡 WebSocket
Conecta-te via navegador ou script a:

bash
Copiar
Editar
ws://localhost:8765
Receberás mensagens como:

scss
Copiar
Editar
📚 Novo livro adicionado! (simulação)
🧪 Testes Automatizados
Autenticação testada via Postman

CRUD de livros testado via curl

Comunicação assíncrona testada via consumidor RabbitMQ

📁 Estrutura do Projeto
css
Copiar
Editar
projeto_biblioteca/
├── cliente-python/
│   └── main.py
├── servidor/
│   ├── rest/          ← REST API + JWT + MongoDB
│   ├── graphql/       ← Apollo Server (GraphQL)
│   ├── soap/          ← node-soap + XML + XSD
│   ├── grpc/          ← gRPC Python
│   ├── websocket/     ← WebSocket Python
│   └── consumidor/    ← RabbitMQ consumer
├── docker-compose.yml
├── .env
└── README.md

👥 Grupo
Martim Nunes - 230000371

Tomás Nunes - 220001350

