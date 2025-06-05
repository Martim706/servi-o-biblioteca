FROM node:18

# Define o diretório de trabalho no container
WORKDIR /app

# Copia apenas os ficheiros de configuração primeiro (melhora cache do Docker)
COPY package*.json ./

# Instala as dependências dentro do container
RUN npm install

# Copia o resto dos ficheiros do projeto
COPY . .

# Comando para iniciar o servidor SOAP
CMD ["node", "server.js"]
