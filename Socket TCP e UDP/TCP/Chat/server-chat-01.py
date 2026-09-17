#!/usr/bin/python3

#---------------------------------------------------------#
# Implementacao de Chat utilizando conexoes TCP. Um lado  #
# comporta-se como cliente e outro como servidor. Este eh #
# o lado servidor.                                        #
#---------------------------------------------------------#
import socket

## Informações do servidor: Host e porta para conexao
Host = ''
Port = 4242

## Criacao do socket TCP e inicio de escuta
socket_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_tcp.bind((Host, Port))
socket_tcp.listen(5)

print ('Bem vindo ao Chat 0.1!!')
# Laco para receber conexoes
while True:
	conn, client_host = socket_tcp.accept()
	print ('Cliente ', client_host, ' conectou.')
	
	# Laco para receber mensagens...
	while True:
		# Recebendo dados ate o tamanho do buffer.
		# Dados maiores sao quebrados em varias mensagens(pacotes)
		data = conn.recv(1024) 
		result = data.decode()
		if not data or result == "EXIT":
			print ("Cliente Desconectou")
			break
	
		# escrevendo mensagem
		print ('=> ', result)

		# enviando msg de volta
		conn.send(result.encode())