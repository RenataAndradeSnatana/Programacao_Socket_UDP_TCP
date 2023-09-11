import socket

serviços = {}  # Dicionário para armazenar informações dos serviços registrados

def servico_registro(nome_servico, host, porta):
    serviços[nome_servico] = (host, porta)

def cancelar_registro_serviço(nome_servico):
    if nome_servico in serviços:
        del serviços[nome_servico]

def lookup_service(nome_servico):
    return serviços.get(nome_servico, None)

def main():
    host = '127.0.0.1'
    porta = 12345

    socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    socket_servidor.bind((host, porta))
    print(f"Servidor de Nomes escutando em {host}:{porta}")

    # Registre o serviço da Calculadora Remota com o nome "Calculator"
    host_calculadora = '127.0.0.1'  # Substitua pelo IP do servidor da Calculadora Remota
    porta_calculadora = 54321  # Porta correta do servidor da Calculadora Remota
    servico_registro("Calculator", host_calculadora, porta_calculadora)

    while True:
        dados, endereco_cliente = socket_servidor.recvfrom(1024)
        mensagem = dados.decode('utf-8')

        if mensagem.startswith("REGISTER"):
            _, nome_servico, service_host, service_port = mensagem.split()
            servico_registro(nome_servico, service_host, int(service_port))
            socket_servidor.sendto("Service registered successfully".encode('utf-8'), endereco_cliente)
        elif mensagem.startswith("UNREGISTER"):
            _, nome_servico = mensagem.split()
            cancelar_registro_serviço(nome_servico)
            socket_servidor.sendto("Service unregistered successfully".encode('utf-8'), endereco_cliente)
        elif mensagem.startswith("LOOKUP"):
            _, nome_servico = mensagem.split()
            info_servidor = lookup_service(nome_servico)
            if info_servidor:
                resposta = f"Service found at {info_servidor[0]}:{info_servidor[1]}"
            else:
                resposta = "Service not found"
            socket_servidor.sendto(resposta.encode('utf-8'), endereco_cliente)
        else:
            socket_servidor.sendto("Invalid command".encode('utf-8'), endereco_cliente)

if __name__ == "__main__":
    main()
