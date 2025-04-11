import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../servidor/grpc'))

import requests
import grpc
import biblioteca_pb2
import biblioteca_pb2_grpc
from zeep import Client

def menu():
    print("""
1. REST - Listar livros
2. GraphQL - Adicionar livro
3. SOAP - Obter livros
4. gRPC - Stream de livros
0. Sair
""")

def usar_rest():
    resp = requests.get('http://localhost:3001/livros')
    livros = resp.json()
    for livro in livros:
        print(f"{livro['id']} - {livro['titulo']} ({livro['ano']}) por {livro['autor']}")

def usar_graphql():
    query = '''
    mutation {
      adicionarLivro(input: {titulo: "Python 101", autor: "João", ano: 2023}) {
        id
        titulo
        autor
        ano
      }
    }
    '''
    resp = requests.post('http://localhost:3002/graphql', json={'query': query})
    print(resp.json())

def usar_soap():
    client = Client('http://localhost:3003/wsdl?wsdl')
    result = client.service.getLivros()
    print(result['livrosXml'])

def usar_grpc():
    channel = grpc.insecure_channel('localhost:50051')
    stub = biblioteca_pb2_grpc.BibliotecaStub(channel)
    for livro in stub.StreamLivros(biblioteca_pb2.Empty()):
        print(f"{livro.id} - {livro.titulo} ({livro.ano}) por {livro.autor}")

if __name__ == "__main__":
    while True:
        menu()
        op = input("Escolha: ")
        if op == "1":
            usar_rest()
        elif op == "2":
            usar_graphql()
        elif op == "3":
            usar_soap()
        elif op == "4":
            usar_grpc()
        elif op == "0":
            break
        else:
            print("Opção inválida.")
