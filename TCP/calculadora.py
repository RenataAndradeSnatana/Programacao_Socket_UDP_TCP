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

    socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_servidor.bind((host, porta))
    socket_servidor.listen(5)
    print(f"Servidor da Calculadora Remota escutando em {host}:{porta}")

    while True:
        cliente_socket, cliente_endereco = socket_servidor.accept()
        dados = cliente_socket.recv(1024).decode('utf-8')

        try:
            comando, num1, num2 = dados.split()
            num1 = float(num1)
            num2 = float(num2)

            if comando == "ADD":
                resultado = soma(num1, num2)
            elif comando == "SUB":
                result = subtracao(num1, num2)
            elif comando == "MUL":
                resultado = multiplicacao(num1, num2)
            elif comando == "DIV":
                resultado = divisao(num1, num2)
            else:
                resultado = "Comando inválido"
        except (ValueError, ZeroDivisionError):
            resultado = "Erro: entrada inválida"

        cliente_socket.send(str(resultado).encode('utf-8'))
        cliente_socket.close()

if __name__ == "__main__":
    main()
