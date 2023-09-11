import socket

def soma(x, y):
    return x + y

def subtracao(x, y):
    return x - y

def multiplicacao(x, y):
    return x * y

def divisao(x, y):
    if y == 0:
        return "Erro: divisão por zero"
    return x / y

def main():
    host = '127.0.0.1'
    porta = 54321

    socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    socket_servidor.bind((host, porta))
    print(f"Servidor da Calculadora Remota escutando em {host}:{porta}")

    while True:
        dados, endereco_cliente = socket_servidor.recvfrom(1024)
        mensagem = dados.decode('utf-8')

        try:
            comando, num1, num2 = mensagem.split()
            num1 = float(num1)
            num2 = float(num2)

            if comando == "ADD":
                resultado = soma(num1, num2)
            elif comando == "SUB":
                resultado = subtracao(num1, num2)
            elif comando == "MUL":
                resultado = multiplicacao(num1, num2)
            elif comando == "DIV":
                resultado = divisao(num1, num2)
            else:
                resultado = "Comando inválido"
        except (ValueError, ZeroDivisionError):
            resultado = "Erro: entrada inválida"

        socket_servidor.sendto(str(resultado).encode('utf-8'), endereco_cliente)

if __name__ == "__main__":
    main()
