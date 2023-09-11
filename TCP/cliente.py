import socket
import time

def main():
    host = '127.0.0.1'
    porta = 12345  # Porta do servidor de nomes (DNS)

    while True:
        entrada = input("Digite o comando (ADD/SUB/MUL/DIV) ou 'QUIT' para sair: ").upper()
        
        if entrada == "QUIT": # Encerra o loop e sai do programa
            break  

        if entrada not in ["ADD", "SUB", "MUL", "DIV"]:
            print("Comando inválido. Use ADD, SUB, MUL ou DIV.")
            continue

        num1 = float(input("Digite o primeiro número: "))
        num2 = float(input("Digite o segundo número: "))
        
        # Marca o tempo inicial
        tempo_inicial = time.time()

        socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_cliente.connect((host, porta))

        # Enviar solicitação para procurar o serviço da Calculadora
        socket_cliente.send(f"LOOKUP Calculator".encode('utf-8')) 
        
        # Receber a resposta do servidor de nomes
        resposta = socket_cliente.recv(1024).decode('utf-8')

        strings_divididas = resposta.split()
       
        if len(strings_divididas) >= 4 and strings_divididas[0] == "Service" and strings_divididas[1] == "found" and strings_divididas[2] == "at":
            endereço_calculadora = strings_divididas[3].split(':')
            host_calculadora = endereço_calculadora[0]
            porta_calculadora = int(endereço_calculadora[1])

            calculator_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            calculator_socket.connect((host_calculadora, porta_calculadora))

            calculator_socket.send(f"{entrada} {num1} {num2}".encode('utf-8'))

            # Receber o resultado da calculadora
            resultado = calculator_socket.recv(1024).decode('utf-8')
            
            # Marca o tempo final
            tempo_final = time.time()

            # Calcula o tempo de envio e recebimento
            tempo_corrido = tempo_final - tempo_inicial
            print(f"Tempo de envio e recebimento: {tempo_corrido} segundos")

            if resultado.startswith("Erro:"):
                print(resultado)
            else:
                print(f"Resultado: {resultado}")

            calculator_socket.close()
        else:
            print("Serviço de calculadora não encontrado.")
        socket_cliente.close()

if __name__ == "__main__":
    main()
