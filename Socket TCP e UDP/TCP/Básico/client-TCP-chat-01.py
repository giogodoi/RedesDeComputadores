#!/usr/bin/python3

#---------------------------------------------------------#
# Implementacao de Chat utilizando conexoes TCP. Um lado  #
# comporta-se como cliente e outro como servidor. Este eh #
# o lado cliente.                                         #
#---------------------------------------------------------#

import socket

## Informacoes do servidor ao qual se conectar
Host = '127.0.0.1'
Port = 4242

## Criacao do socket para comunicacao
socket_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_tcp.connect((Host, Port))

print ('Bem vindo ao Chat 0.1!!')
## laco para enviar mensagens
while True:
	## lendo mensagem
	msg = input("=> ")

	# enviando
	socket_tcp.send(msg.encode())

	if msg == "EXIT":
		print ("Fim de chat")
		break
	pass

pass

socket_tcp.close()
