
const express = require('express');
const fs = require('fs');
const path = require('path');
const app = express();
const PORT = 3001;

app.use(express.json());

const dataPath = path.join(__dirname, 'livros.json');

// Função utilitária para ler os dados
function readData() {
    if (!fs.existsSync(dataPath)) return [];
    const jsonData = fs.readFileSync(dataPath);
    return JSON.parse(jsonData);
}

// Função utilitária para escrever os dados
function writeData(data) {
    fs.writeFileSync(dataPath, JSON.stringify(data, null, 2));
}

// CRUD Endpoints

// GET - Listar todos os livros
app.get('/livros', (req, res) => {
    const livros = readData();
    res.json(livros);
});

// POST - Adicionar novo livro
app.post('/livros', (req, res) => {
    const livros = readData();
    const novoLivro = { id: Date.now(), ...req.body };
    livros.push(novoLivro);
    writeData(livros);
    res.status(201).json(novoLivro);
});

// PUT - Atualizar livro por ID
app.put('/livros/:id', (req, res) => {
    const livros = readData();
    const id = parseInt(req.params.id);
    const index = livros.findIndex(l => l.id === id);
    if (index === -1) return res.status(404).json({ error: 'Livro não encontrado' });
    livros[index] = { ...livros[index], ...req.body };
    writeData(livros);
    res.json(livros[index]);
});

// DELETE - Remover livro por ID
app.delete('/livros/:id', (req, res) => {
    let livros = readData();
    const id = parseInt(req.params.id);
    const livro = livros.find(l => l.id === id);
    if (!livro) return res.status(404).json({ error: 'Livro não encontrado' });
    livros = livros.filter(l => l.id !== id);
    writeData(livros);
    res.json({ mensagem: 'Livro removido' });
});

// Exportar dados em JSON
app.get('/exportar/json', (req, res) => {
    const livros = readData();
    res.setHeader('Content-Disposition', 'attachment; filename=livros.json');
    res.json(livros);
});

// Importar dados JSON
app.post('/importar/json', (req, res) => {
    const novosLivros = req.body;
    writeData(novosLivros);
    res.json({ mensagem: 'Dados importados com sucesso!' });
});

app.listen(PORT, () => {
    console.log(`Servidor REST a correr em http://localhost:${PORT}`);
});
