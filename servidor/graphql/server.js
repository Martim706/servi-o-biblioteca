
const express = require('express');
const { graphqlHTTP } = require('express-graphql');
const { buildSchema } = require('graphql');
const fs = require('fs');
const path = require('path');

const app = express();
const PORT = 3002;

const dataPath = path.join(__dirname, 'livros.json');

function readData() {
  if (!fs.existsSync(dataPath)) return [];
  const data = fs.readFileSync(dataPath);
  return JSON.parse(data);
}

function writeData(data) {
  fs.writeFileSync(dataPath, JSON.stringify(data, null, 2));
}

// Schema GraphQL
const schema = buildSchema(\`
  type Livro {
    id: Int
    titulo: String
    autor: String
    ano: Int
  }

  type Query {
    livros: [Livro]
    livro(id: Int!): Livro
  }

  input LivroInput {
    titulo: String
    autor: String
    ano: Int
  }

  type Mutation {
    adicionarLivro(input: LivroInput): Livro
    atualizarLivro(id: Int!, input: LivroInput): Livro
    removerLivro(id: Int!): String
  }
\`);

const root = {
  livros: () => readData(),
  livro: ({ id }) => readData().find(l => l.id === id),
  adicionarLivro: ({ input }) => {
    const livros = readData();
    const novo = { id: Date.now(), ...input };
    livros.push(novo);
    writeData(livros);
    return novo;
  },
  atualizarLivro: ({ id, input }) => {
    const livros = readData();
    const index = livros.findIndex(l => l.id === id);
    if (index === -1) return null;
    livros[index] = { ...livros[index], ...input };
    writeData(livros);
    return livros[index];
  },
  removerLivro: ({ id }) => {
    let livros = readData();
    livros = livros.filter(l => l.id !== id);
    writeData(livros);
    return "Removido com sucesso";
  }
};

app.use('/graphql', graphqlHTTP({
  schema: schema,
  rootValue: root,
  graphiql: true
}));

app.listen(PORT, () => {
  console.log(`Servidor GraphQL a correr em http://localhost:\${PORT}/graphql`);
});
