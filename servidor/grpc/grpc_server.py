from concurrent import futures
import grpc
import time
import biblioteca_pb2
import biblioteca_pb2_grpc

# Dados de exemplo (podem ser ligados ao MongoDB ou outro serviço real)
LIVROS = [
    {"id": 1, "titulo": "Livro A", "autor": "Autor 1", "ano": 2020},
    {"id": 2, "titulo": "Livro B", "autor": "Autor 2", "ano": 2021},
    {"id": 3, "titulo": "Livro C", "autor": "Autor 3", "ano": 2022},
]

class BibliotecaService(biblioteca_pb2_grpc.BibliotecaServicer):
    def GetLivroPorID(self, request, context):
        for livro in LIVROS:
            if livro["id"] == request.id:
                return biblioteca_pb2.Livro(
                    id=livro["id"],
                    titulo=livro["titulo"],
                    autor=livro["autor"],
                    ano=livro["ano"]
                )
        context.set_code(grpc.StatusCode.NOT_FOUND)
        context.set_details("Livro não encontrado")
        return biblioteca_pb2.Livro()

    def StreamLivros(self, request, context):
        for livro in LIVROS:
            yield biblioteca_pb2.Livro(
                id=livro["id"],
                titulo=livro["titulo"],
                autor=livro["autor"],
                ano=livro["ano"]
            )
            time.sleep(0.5)  # Simula envio gradual

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    biblioteca_pb2_grpc.add_BibliotecaServicer_to_server(BibliotecaService(), server)
    server.add_insecure_port("[::]:50051")
    print("Servidor gRPC ativo na porta 50051...")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
