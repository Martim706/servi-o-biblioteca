const http = require('http');
const soap = require('soap');
const fs = require('fs');
const path = require('path');
const libxmljs = require('libxmljs2');

const livrosPath = path.join(__dirname, 'livros.xml');
const xsdPath = path.join(__dirname, 'livros.xsd');

// Função para obter livros (sem alterações)
function getLivros(callback) {
    fs.readFile(livrosPath, 'utf8', (err, data) => {
        if (err) return callback({ erro: 'Erro ao ler XML' });
        callback({ livrosXml: data });
    });
}

// Função para adicionar livro com validação XML contra XSD
function addLivro(args, callback) {
    const novoLivroXml = `
<livro>
  <titulo>${args.titulo}</titulo>
  <autor>${args.autor}</autor>
  <ano>${args.ano}</ano>
</livro>`;

    let livrosXml = '';
    if (fs.existsSync(livrosPath)) {
        livrosXml = fs.readFileSync(livrosPath, 'utf8').trim();
        livrosXml = livrosXml.replace('</livros>', novoLivroXml + '\n</livros>');
    } else {
        livrosXml = `<?xml version="1.0"?>\n<livros>${novoLivroXml}\n</livros>`;
    }

    try {
        const xmlDoc = libxmljs.parseXml(livrosXml);
        const xsdDoc = libxmljs.parseXml(fs.readFileSync(xsdPath, 'utf8'));

        if (!xmlDoc.validate(xsdDoc)) {
            const errors = xmlDoc.validationErrors.map(e => e.message).join('\n');
            return callback({ erro: `Erro de validação do XML:\n${errors}` });
        }

        fs.writeFileSync(livrosPath, livrosXml);
        callback({ resultado: 'Livro adicionado com sucesso!' });

    } catch (err) {
        callback({ erro: 'Erro ao validar XML: ' + err.message });
    }
}

const service = {
    BibliotecaService: {
        BibliotecaPort: {
            getLivros: function (_, callback) {
                getLivros(callback);
            },
            addLivro: function (args, callback) {
                addLivro(args, callback);
            }
        }
    }
};

const xmlWsdl = fs.readFileSync(path.join(__dirname, 'biblioteca.wsdl'), 'utf8');
const server = http.createServer((req, res) => res.end('SOAP server'));
server.listen(3003, () => {
    soap.listen(server, '/wsdl', service, xmlWsdl);
    console.log('Servidor SOAP a correr em http://localhost:3003/wsdl');
});

