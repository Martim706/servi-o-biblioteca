
const fs = require('fs');
const path = require('path');
const grpc = require('@grpc/grpc-js');
const protoLoader = require('@grpc/proto-loader');

const livrosPath = path.join(__dirname, 'livros.json');

function readData() {
  if (!fs.existsSync(livrosPath)) return [];
  const data = fs.readFileSync(livrosPath);
  return JSON.parse(data);
}

function writeData(data) {
  fs.writeFileSync(livrosPath, JSON.stringify(data, null, 2));
}

const packageDefinition = protoLoader.loadSync('biblioteca.proto', {});
const proto = grpc.loadPackageDefinition(packageDefinition).biblioteca;

function ListarLivros(_, callback) {
  const livros = readData();
  callback(null, { livros });
}

function AdicionarLivro(call, callback) {
  const livros = readData();
  const novo = { id: Date.now(), ...call.request };
  livros.push(novo);
  writeData(livros);
  callback(null, novo);
}

function StreamLivros(call) {
  const livros = readData();
  livros.forEach(livro => call.write(livro));
  call.end();
}

const server = new grpc.Server();
server.addService(proto.Biblioteca.service, {
  ListarLivros,
  AdicionarLivro,
  StreamLivros
});

server.bindAsync('0.0.0.0:50051', grpc.ServerCredentials.createInsecure(), () => {
  console.log('Servidor gRPC ativo em http://localhost:50051');
  server.start();
});
