import socket

#---------------------------------------------------------#
# Implementação de Chat utilizando UDP. Este é o lado     #
# servidor.                                               #
#---------------------------------------------------------#

## Informações do servidor: Host e porta para conexão
Host = ''
Port = 4242

## Criação do socket UDP
socket_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socket_udp.bind((Host, Port))

print ('Bem vindo ao Chat UDP!!')

# Laço para receber mensagens
while True:
    # Recebendo dados até o tamanho do buffer.
    # O método recvfrom retorna os dados e o endereço do cliente
    data, client_host = socket_udp.recvfrom(1024) 
    
    # Decodifica a mensagem recebida
    result = data.decode('utf-8')
    
    # Se a mensagem for "EXIT", o cliente está saindo
    if result == "EXIT":
        print ("Cliente ", client_host, " saiu.")
        # Podemos continuar o loop para aguardar outros clientes
        continue 
    
    retorno = f'Mensagem de {client_host}: {result}'
    print (retorno)
    socket_udp.sendto(retorno.encode('utf-8'), client_host)

    # Enviando de volta a mesma mensagem para o cliente que enviou
    socket_udp.sendto(data, client_host)