#!/usr/bin/python3

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
	
	data = socket_tcp.recv(1024) 
	result = data.decode()
	# escrevendo mensagem
	print ('=> ', result)

socket_tcp.close()