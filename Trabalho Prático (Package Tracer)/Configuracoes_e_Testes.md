# Relatório de Configuração - Trabalho 1 (Packet Tracer)

## Informações Gerais

Disciplina: Redes de Computadores

Professor: Hermes Pimenta de Moraes Júnior

Alunos: Giovane Felipe Godoi Oliveira, Luiz Fellipe Resende Lima, Vincent Collares Biazotti

## Topologia e Opções de Endereçamento IP

A topologia lógica foi construída utilizando uma topologia em estrela centralizada em um único Switch, conectando 6 hosts e 2 servidores.

Para o endereçamento, optou-se pela utilização da rede IPv4 privada 192.168.1.0/24. Esta é uma rede de Classe C padrão, ideal para ambientes locais pequenos (LAN), oferecendo uma máscara de sub-rede 255.255.255.0 que comporta até 254 dispositivos.

Para manter a organização lógica, os IPs foram separados em blocos:

Servidores: Receberam os primeiros endereços disponíveis na rede.

Servidor 1 (Web/FTP): 192.168.1.10

Servidor 2 (DNS): 192.168.1.11

Hosts (Clientes): Receberam endereços a partir do sufixo 100 para rápida identificação.

Hosts 1 ao 6: 192.168.1.101 a 192.168.1.106

Todos os hosts foram configurados com o parâmetro "DNS Server" apontando para o IP 192.168.1.11, garantindo que os clientes conseguissem traduzir os nomes de domínio criados para os respectivos IPs.

## Testes Realizados

Para validar os requisitos do trabalho, foram executadas simulações e testes de conectividade a partir dos hosts (clientes) em direção aos servidores:

Teste de Resolução DNS e Conectividade (Ping)
A partir do prompt de comando (Command Prompt) de um host, foram disparados pacotes ICMP (Ping) para os domínios www.gcc125.ufla.br e ftp.gcc125.ufla.br. O teste confirmou que o Servidor DNS traduziu corretamente os nomes para o IP 192.168.1.10 e que havia comunicação física e lógica na rede.

Teste do Servidor Web (HTTP)
Através do Web Browser integrado nos hosts, foi acessado o endereço www.gcc125.ufla.br. A página carregou com sucesso, exibindo a estrutura em HTML contendo o nome da disciplina, o nome do professor, o nome dos alunos integrantes do grupo e as credenciais necessárias para o acesso posterior ao FTP.

Teste do Servidor FTP (Transferência de Arquivos)
Pelo Command Prompt dos hosts, foi iniciada uma sessão FTP com o comando ftp ftp.gcc125.ufla.br. O acesso foi concedido após a inserção do usuário e senha definidos (usuário: aluno, senha: redes123).
Para validar as permissões:

Download: Foi executado o comando get para baixar um arquivo de texto previamente criado no servidor.

Upload: Foi executado o comando put para enviar um arquivo de teste criado localmente no host (via Text Editor) para o diretório raiz do servidor FTP. Ambos os testes confirmaram a permissão de leitura e escrita do usuário.