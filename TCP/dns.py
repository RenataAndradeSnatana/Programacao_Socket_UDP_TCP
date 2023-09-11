import socket

serviços = {} # Dicionário para armazenar informações dos serviços registrados

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

    socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_servidor.bind((host, porta))
    socket_servidor.listen(5)
    print(f"Servidor de Nomes escutando em {host}:{porta}")

    # Registre o serviço da Calculadora Remota com o nome "Calculator"
    host_calculadora = '127.0.0.1'  # Substitua pelo IP do servidor da Calculadora Remota
    porta_calculadora = 54321  # Porta correta do servidor da Calculadora Remota
    servico_registro("Calculator", host_calculadora, porta_calculadora)

    while True:
        socket_cliente, endereco_cliente = socket_servidor.accept()
        dados = socket_cliente.recv(1024).decode('utf-8')

        if dados.startswith("REGISTER"):
            _, nome_servico, service_host, service_port = dados.split()
            servico_registro(nome_servico, service_host, int(service_port))
            socket_cliente.send("Service registered successfully".encode('utf-8'))
        elif dados.startswith("UNREGISTER"):
            _, nome_servico = dados.split()
            cancelar_registro_serviço(nome_servico)
            socket_cliente.send("Service unregistered successfully".encode('utf-8'))
        elif dados.startswith("LOOKUP"):
            _, nome_servico = dados.split()
            info_servidor = lookup_service(nome_servico)
            if info_servidor:
                socket_cliente.send(f"Service found at {info_servidor[0]}:{info_servidor[1]}".encode('utf-8'))
            else:
                socket_cliente.send("Service not found".encode('utf-8'))
        else:
            socket_cliente.send("Invalid command".encode('utf-8'))

        socket_cliente.close()

if __name__ == "__main__":
    main()
