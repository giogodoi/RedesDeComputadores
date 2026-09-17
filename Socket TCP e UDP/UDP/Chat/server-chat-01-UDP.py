import socket

# Informações do servidor: Host e porta para conexão
Host = ''
Port = 4242

# Criação do socket UDP
socket_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socket_udp.bind((Host, Port))

print('Bem-vindo ao Chat 0.1!! (UDP)')
# Laço para receber mensagens
while True:
    # Recebendo dados e endereço do cliente
    data, client_host = socket_udp.recvfrom(1024)
    result = data.decode()

    # Se a mensagem for "EXIT", encerra o chat com o cliente
    if not data or result == "EXIT":
        print("Cliente finalizou a convera")
        break

    # Exibindo mensagem recebida
    print('=> ', result)

    # Lendo resposta do servidor
    msg = input("=> ")

    # Enviando resposta de volta ao cliente
    socket_udp.sendto(msg.encode(), client_host)