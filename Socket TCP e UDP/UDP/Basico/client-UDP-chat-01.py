import socket

## Informações do servidor: Host e porta para conexão
Host = ''
Port = 4242

## Criação do socket UDP
socket_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socket_udp.bind((Host, Port))

clientes_conectados = set()


# Laço para receber mensagens
while True:
    # Recebendo dados até o tamanho do buffer
    data, client_host = socket_udp.recvfrom(1024)
    
    # Decodifica a mensagem recebida
    result = data.decode('utf-8')
    
    # Se o cliente não estiver na lista, nós o adicionamos
    if client_host not in clientes_conectados:
        clientes_conectados.add(client_host)
        print(f"Novo cliente conectado: {client_host}")
    
    # Se a mensagem for "EXIT", o cliente está saindo
    if result == "EXIT":
        print(f"Cliente {client_host} saiu.")
        clientes_conectados.remove(client_host) # Remove da lista de disparos
        continue
        
    # Formata a mensagem especificando o IP/Porta de quem enviou
    retorno = f'Mensagem de {client_host}: {result}'
    print(retorno)
    
    # Dispara a mensagem para TODOS os clientes da lista (Broadcast)
    for cliente in clientes_conectados:
        # Codifica o texto formatado para enviar a todos
        socket_udp.sendto(retorno.encode('utf-8'), cliente)
