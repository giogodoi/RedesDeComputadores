#!/usr/bin/python3

#---------------------------------------------------------#
# Implementacao de cliente para Chat utilizando UDP.      #
#---------------------------------------------------------#

import socket

# Informações do servidor ao qual se conectar
Host = '127.0.0.1'
Port = 4242

# Criação do socket UDP
socket_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print('Bem-vindo ao Chat 0.1!! (UDP)')
# Laço para enviar mensagens
while True:
    # Lendo mensagem do cliente
    msg = input("=> ")

    # Enviando mensagem para o servidor
    socket_udp.sendto(msg.encode(), (Host, Port))

    # Encerra o chat se a mensagem for "EXIT"
    if msg == "EXIT":
        print("Fim de chat")
        break

    # Recebendo resposta do servidor
    data, _ = socket_udp.recvfrom(1024)
    result = data.decode()
    
    # Exibindo mensagem recebida
    print('=> ', result)

socket_udp.close()