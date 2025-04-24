import express from 'express';
import { graphqlHTTP } from 'express-graphql';
import { buildSchema } from 'graphql';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { dirname } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const livrosPath = path.join(__dirname, 'livros.json');

function readData() {
  if (!fs.existsSync(livrosPath)) return [];
  const data = fs.readFileSync(livrosPath);
  return JSON.parse(data);
}

function writeData(data) {
  fs.writeFileSync(livrosPath, JSON.stringify(data, null, 2));
}

const schema = buildSchema(`
  type Livro {
    id: Float
    titulo: String
    autor: String
    ano: Int
  }

  input LivroInput {
    id: Float
    titulo: String
    autor: String
    ano: Int
  }

  type Query {
    livros: [Livro]
  }

  type Mutation {
    adicionarLivro(input: LivroInput): Livro
  }
`);

const root = {
  livros: () => readData(),
  adicionarLivro: ({ input }) => {
    const livros = readData();
    const novo = { ...input, id: Date.now() };
    livros.push(novo);
    writeData(livros);
    return novo;
  }
};

const app = express();
app.use('/graphql', graphqlHTTP({
  schema,
  rootValue: root,
  graphiql: true
}));

app.listen(3002, () => {
  console.log('Servidor GraphQL a correr em http://localhost:3002/graphql');
});

