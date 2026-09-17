import socket
import threading

## Informacoes do servidor ao qual se conectar
Host = '192.168.103.11'
Port = 5050

## Criacao do socket TCP para comunicacao
socket_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_tcp.connect((Host, Port))

#################################################################
## Funcao para enviar mensagens para o servidor                ##
#################################################################
def enviar():
    while True:
        message = input("=> ")
        # da encode na mensagem do cliente e a envia ao servidor 
        socket_tcp.send(message.encode())
        # se a mensagem for 'EXIT' encerra esta funcao
        if message == "EXIT":
            print ("Você desconectou!")
            break
    return
#################################################################
## Funcao para receber mensagens do servidor                   ##
#################################################################
def receber():
    while True:
        #recebe a mensagem do servidor, buffer de tamanho 1024
        message = socket_tcp.recv(1024)
        #Se a mensagem do servidor for 'EXIT' significa que este mesmo cliente encerrou 
        # este programa, entao encerramos essa thread e 
        # finalizamos o socket
        if message.decode() == "EXIT":
            socket_tcp.close()
            break
        #caso contrario continuaremos a execucao normal da funcao e imprimimos a mensagem
        elif message:
            print('\n', message.decode(), '\n')
    return

#########################
## Programa principal ###
#########################
print ('Bem vindo ao Chat 0.3!!')
#cria-se duas threads, uma para receber e outra para enviar
t1 = threading.Thread(target=receber)
t2 = threading.Thread(target=enviar)
#inicia as duas threads
t1.start()
t2.start()
