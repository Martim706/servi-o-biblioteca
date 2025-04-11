
# 📚 Projeto Biblioteca - Integração de Sistemas

Este projeto demonstra um sistema de gestão de livros utilizando múltiplas tecnologias de serviços web.

## ✅ Tecnologias Implementadas

- **REST (Express.js)** – CRUD completo
- **GraphQL (Express + GraphQL)** – Queries e mutations
- **SOAP (node-soap)** – Operações XML com WSDL e XSD
- **gRPC (grpc-js)** – Operações unárias e streaming
- **Cliente Python** – Integra com todos os serviços
- **Persistência** – Arquivos `.json` e `.xml`
- **Docker** – Configuração com Dockerfile e docker-compose

## ▶️ Como Executar

### Pré-requisitos

- Node.js
- Python 3
- Docker (opcional)

### Instalação (modo manual)

```bash
# REST
cd servidor/rest
npm install
node server.js

# GraphQL
cd ../graphql
npm install
node server.js

# SOAP
cd ../soap
npm install node-soap
node server.js

# gRPC
cd ../grpc
npm install @grpc/grpc-js @grpc/proto-loader
node server.js
```

### Cliente Python

```bash
pip install requests zeep grpcio grpcio-tools
cd cliente
python cliente.py
```

## 🧪 Exemplos de Uso

### REST

- `GET /livros` – Lista todos os livros
- `POST /livros` – Adiciona livro
- `PUT /livros/:id` – Atualiza
- `DELETE /livros/:id` – Remove
- `GET /exportar/json` – Exportar JSON
- `POST /importar/json` – Importar JSON

### GraphQL

Acesso: `http://localhost:3002/graphql` com interface GraphiQL

```graphql
query {
  livros {
    id
    titulo
    autor
    ano
  }
}
```

### SOAP

- WSDL disponível em: `http://localhost:3003/wsdl?wsdl`

### gRPC

- Servidor em `localhost:50051`
- Métodos: `ListarLivros`, `AdicionarLivro`, `StreamLivros`

---

## 📁 Estrutura do Projeto

```
projeto_biblioteca_completo/
├── cliente/
│   └── cliente.py
├── servidor/
│   ├── rest/
│   ├── graphql/
│   ├── soap/
│   └── grpc/
├── documentacao/
├── docker-compose.yml
└── README.md
```
