## Este é um documento adicional que visa explicitar os aprendizados com a primeira etapa do trabalho de instalação.

# Tutorial – Etapa 1: Sincronização de Hora e Servidor Web em VMs Debian

Redes de Computadores – UFLA – Prof. Hermes Pimenta de Moraes Júnior
Grupo: Giovane Felipe Godoi Oliveira, Luis Fellipe Resende Lima e Vincent Biazotti Collares (Turma 10A)

Este tutorial reúne, em ordem, todos os comandos usados para configurar as duas VMs do trabalho. Seguindo-o do início ao fim, é possível replicar a configuração em outro par de VMs Debian.

---

## 0. Visão geral

| VM | Hostname | IP | Serviços |
| --- | --- | --- | --- |
| VM1 | vm07 | 192.168.1.7 | Sincronização de hora (Chrony): cliente do NTP.br e servidor para a VM2 |
| VM2 | vm08 | 192.168.1.8 | Servidor Web (Apache) com HTTP e HTTPS; cliente de hora da VM1 |

- Sistema das VMs: Debian 11.11 (bullseye).
- Acesso: SSH através da VPN do Laboratório Virtual (rede das VMs: `192.168.1.0/24`).
- **Para replicar com outras VMs**, substitua `192.168.1.7` pelo IP da sua VM1 e `192.168.1.8` pelo IP da sua VM2 em todos os comandos.

**Onde rodar cada comando.** Cada bloco indica o local:

- 🖥️ **PC**: o seu computador (prompt local)
- 🕐 **VM1**: prompt `aluno@vm07`
- 🌐 **VM2**: prompt `aluno@vm08`

> **Dica:** rode um comando por vez e confira o prompt antes. Se o seu terminal for **zsh**, não cole comandos com comentários (`# ...`): o zsh não trata `#` como comentário por padrão, e o comando pode ir parar no lugar errado.

**Restrições do enunciado:**

- Não altere nem apague os usuários `moraes` e `mendes`.
- Não instale nem configure firewall.

---

## 1. VPN do Laboratório Virtual (🖥️ PC)

### 1.1 Debian / Ubuntu

```bash
sudo apt install -y network-manager-openvpn-gnome
```

### 1.2 Fedora

O tutorial da disciplina é para Debian e Ubuntu. No Fedora, o pacote tem outro nome:

```bash
sudo dnf install -y NetworkManager-openvpn-gnome
```

### 1.3 Importar e conectar

Baixe o `laboratorio.ovpn` do Campus Virtual. Se o navegador abrir o conteúdo como texto, salve com **Ctrl+S** ou copie o texto para um arquivo `laboratorio.ovpn`. Os certificados e a chave já vêm embutidos no arquivo.

Importe o perfil (ajuste o caminho do arquivo):

```bash
nmcli connection import type openvpn file ~/caminho/para/laboratorio.ovpn
```

Defina o usuário, que é o e-mail institucional sem `@estudante.ufla.br`:

```bash
nmcli connection modify laboratorio vpn.user-name SEU.USUARIO
```

Opcional, para mandar pela VPN só o tráfego do laboratório:

```bash
nmcli connection modify laboratorio ipv4.never-default yes
```

Conecte. O comando pede a senha dos sistemas da UFLA:

```bash
nmcli connection up laboratorio --ask
```

### 1.4 Verificar

```bash
ip -br a | grep tun0
ip route | grep tun0
```

Esperado: uma interface `tun0` com IP `192.168.2.x` e uma rota para `192.168.1.0/24` (a rede das VMs).

Para desconectar:

```bash
nmcli connection down laboratorio
```

**Alternativa**, se o NetworkManager der problema:

```bash
sudo dnf install -y openvpn
sudo openvpn --config ~/caminho/para/laboratorio.ovpn
```

Espere aparecer `Initialization Sequence Completed` e deixe esse terminal aberto.

---

## 2. Primeiro acesso às VMs (🕐 VM1 e 🌐 VM2)

### 2.1 Conectar e trocar a senha

Faça isto em **cada** VM. A senha inicial é `aluno`:

```bash
ssh aluno@192.168.1.7
```

```bash
passwd
```

Depois repita com `ssh aluno@192.168.1.8`.

### 2.2 Conferir a VM

```bash
sudo -v
hostname
ip -br a
cat /etc/debian_version
ping -c3 a.ntp.br
```

- `sudo -v` pede a senha nova e não imprime nada quando dá certo.
- `ping a.ntp.br` confirma que a VM tem internet e resolução de nomes.

Opcional, no 🖥️ PC, para não digitar a senha a cada acesso:

```bash
ssh-copy-id aluno@192.168.1.7
ssh-copy-id aluno@192.168.1.8
```

---

## 3. Sincronização de hora com Chrony

Arquitetura: **NTP.br → VM1 (stratum 2) → VM2 (stratum 3)**.

### 3.1 VM1: cliente do NTP.br e servidor para a VM2 (🕐 VM1)

Instale o Chrony. Ele substitui automaticamente o `systemd-timesyncd`:

```bash
sudo apt update
sudo apt install -y chrony
```

Ajuste o fuso horário:

```bash
sudo timedatectl set-timezone America/Sao_Paulo
```

Desative o pool padrão do Debian e as fontes recebidas por DHCP:

```bash
sudo sed -i -e 's/^pool /#pool /' -e 's/^sourcedir /#sourcedir /' /etc/chrony/chrony.conf
```

Adicione os servidores do NTP.br e libere a VM2 como cliente:

```bash
sudo tee -a /etc/chrony/chrony.conf > /dev/null << 'EOF'

server a.st1.ntp.br iburst
server b.st1.ntp.br iburst
server c.st1.ntp.br iburst
server d.st1.ntp.br iburst
server a.ntp.br iburst
server b.ntp.br iburst
server gps.ntp.br iburst

allow 192.168.1.8
local stratum 10
EOF
```

- `allow` autoriza a VM2 a consultar a hora na VM1.
- `local stratum 10` mantém a VM1 servindo hora mesmo se perder acesso ao NTP.br.

Reinicie o serviço e ative-o na inicialização:

```bash
sudo systemctl restart chrony
sudo systemctl enable chrony
```

Confira o arquivo final (mostra só as linhas ativas):

```bash
grep -Ev '^\s*(#|$)' /etc/chrony/chrony.conf
```

### 3.2 VM2: cliente da VM1 (🌐 VM2)

```bash
sudo apt update
sudo apt install -y chrony
sudo timedatectl set-timezone America/Sao_Paulo
```

Desative o pool padrão **e** o `sourcedir`. Sem isso, a VM2 continua pegando hora da internet em vez da VM1:

```bash
sudo sed -i -e 's/^pool /#pool /' -e 's/^sourcedir /#sourcedir /' /etc/chrony/chrony.conf
```

Defina a VM1 como única fonte. O comando só adiciona a linha se ela ainda não existir:

```bash
grep -q '^server 192.168.1.7' /etc/chrony/chrony.conf || echo "server 192.168.1.7 iburst prefer" | sudo tee -a /etc/chrony/chrony.conf
```

Reinicie o serviço e ative-o na inicialização:

```bash
sudo systemctl restart chrony
sudo systemctl enable chrony
```

Confira o arquivo. Não deve haver linhas `pool` nem `sourcedir`, e deve aparecer `server 192.168.1.7 iburst prefer`:

```bash
grep -Ev '^\s*(#|$)' /etc/chrony/chrony.conf
```

### 3.3 Verificação da hora

Espere uns 30 segundos depois de reiniciar o Chrony antes de verificar.

🕐 **VM1:**

```bash
chronyc sources -v
chronyc tracking
timedatectl
```

Esperado:

- um servidor do NTP.br marcado com `^*`;
- `Stratum : 2` e `Leap status : Normal`;
- `System clock synchronized: yes` e o fuso `America/Sao_Paulo`.

🌐 **VM2:**

```bash
chronyc sources -v
chronyc tracking
```

Esperado:

- uma única fonte, `^* 192.168.1.7`;
- `Reference ID ... (192.168.1.7)` e `Stratum : 3`.

🕐 **VM1**, para confirmar que a VM2 é cliente:

```bash
sudo chronyc clients
```

Esperado: o IP `192.168.1.8` na lista, com contagem de pacotes NTP.

### 3.4 Teste de correção do relógio (🌐 VM2)

Mude o relógio de propósito:

```bash
sudo date -s "2020-01-01 00:00:00"
date
```

Force uma nova medição da VM1 e espere uns 10 segundos:

```bash
sudo chronyc burst 4/4
```

Opcional, para ver o desvio enorme detectado:

```bash
chronyc sources
```

Aplique a correção:

```bash
sudo chronyc makestep
date
```

O último `date` deve mostrar a data e a hora corretas.

> **Atenção:** rodar `makestep` logo após o `date -s` não corrige nada. O Chrony usa a última medição, feita antes da alteração, que ainda indicava desvio quase zero. Por isso o `burst` vem antes.

---

## 4. Servidor Web com Apache (🌐 VM2)

### 4.1 Instalar o Apache

```bash
sudo apt install -y apache2
sudo systemctl enable --now apache2
```

O `curl` não vem instalado na VM (só a biblioteca `libcurl4`). Instale para os testes:

```bash
sudo apt install -y curl
```

Teste:

```bash
curl -I http://localhost
```

Esperado: `HTTP/1.1 200 OK`.

### 4.2 Pastas do site e permissões

```bash
sudo mkdir -p /var/www/html/relatorios /var/www/html/trabalhos
sudo chown -R aluno:www-data /var/www/html
sudo chmod -R 755 /var/www/html
```

### 4.3 HTTPS com certificado autoassinado

Gere o certificado, válido por 1 ano e emitido para o IP da VM2:

```bash
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/ssl/private/grupo.key -out /etc/ssl/certs/grupo.crt -subj "/C=BR/ST=MG/L=Lavras/O=UFLA/OU=DCC/CN=192.168.1.8" -addext "subjectAltName=IP:192.168.1.8"
```

Ative o módulo SSL:

```bash
sudo a2enmod ssl
```

Troque o certificado padrão (snakeoil) pelo certificado do grupo:

```bash
sudo sed -i -e 's#/etc/ssl/certs/ssl-cert-snakeoil.pem#/etc/ssl/certs/grupo.crt#' -e 's#/etc/ssl/private/ssl-cert-snakeoil.key#/etc/ssl/private/grupo.key#' /etc/apache2/sites-available/default-ssl.conf
```

Confira a troca. Devem aparecer `grupo.crt` e `grupo.key`:

```bash
grep -E 'SSLCertificate(File|KeyFile)' /etc/apache2/sites-available/default-ssl.conf
```

Ative o site HTTPS, teste a configuração e recarregue o Apache:

```bash
sudo a2ensite default-ssl
sudo apache2ctl configtest
sudo systemctl reload apache2
```

O `configtest` precisa retornar `Syntax OK`.

Opcional, para eliminar o aviso `AH00558` sobre o nome do servidor:

```bash
echo "ServerName 192.168.1.8" | sudo tee /etc/apache2/conf-available/servername.conf
sudo a2enconf servername
sudo systemctl reload apache2
```

> **Não** configure redirecionamento de HTTP para HTTPS. O enunciado pede que o servidor atenda pelos **dois** protocolos.

### 4.4 Página principal

```bash
cat > /var/www/html/index.html << 'EOF'
<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Redes de Computadores - Turma 10A</title>
<style>
 body{font-family:sans-serif;max-width:800px;margin:40px auto;padding:0 16px;line-height:1.6;color:#222}
 h1{border-bottom:2px solid #0a5;padding-bottom:8px}
 table{border-collapse:collapse;width:100%} td,th{border:1px solid #999;padding:6px 12px;text-align:left}
 th{background:#eee}
</style>
</head>
<body>
<h1>Redes de Computadores</h1>
<p>Universidade Federal de Lavras – Departamento de Ciência da Computação<br>
Prof. Hermes Pimenta de Moraes Júnior</p>

<h2>Integrantes – Turma 10A</h2>
<ul>
 <li>Giovane Felipe Godoi Oliveira</li>
 <li>Luis Fellipe Resende Lima</li>
 <li>Vincent Biazotti Collares</li>
</ul>

<h2>Máquinas Virtuais</h2>
<table>
 <tr><th>VM</th><th>IP</th><th>Serviços</th></tr>
 <tr><td>vm07</td><td>192.168.1.7</td><td>Sincronização de hora (Chrony) • DNS (etapa 2)</td></tr>
 <tr><td>vm08</td><td>192.168.1.8</td><td>Web HTTP/HTTPS (Apache) • FTP (etapa 2)</td></tr>
</table>

<h2>Relatórios</h2>
<ul>
 <li><a href="relatorios/relatorio-etapa1.pdf">Relatório – Etapa 1: Sincronização de Hora e Servidor Web</a></li>
</ul>

<h2>Trabalhos da disciplina</h2>
<ul>
 <li><a href="trabalhos/">Repositório de trabalhos (Packet Tracer e demais entregas)</a></li>
</ul>
</body>
</html>
EOF
```

A pasta `trabalhos/` é listada automaticamente pelo Apache, porque a opção `Indexes` já vem ativa no Debian.

### 4.5 Enviar relatório e trabalhos (🖥️ PC)

Envie o relatório:

```bash
scp relatorio-etapa1.pdf aluno@192.168.1.8:/var/www/html/relatorios/
```

Envie a pasta de trabalhos. Como ela é um repositório Git, o comando exclui a pasta `.git` e mantém as subpastas (ajuste o caminho):

```bash
tar --exclude=.git -czf - -C /caminho/ate/a/pasta-pai RedesDeComputadores | ssh aluno@192.168.1.8 "tar -xzf - -C /var/www/html/trabalhos/"
```

Para **atualizar** a pasta depois, rode o mesmo comando de novo. Se alguma pasta foi renomeada ou apagada, remova a cópia antiga antes:

```bash
ssh aluno@192.168.1.8 "rm -rf /var/www/html/trabalhos/RedesDeComputadores"
```

O HTTP e o HTTPS servem a mesma pasta (`/var/www/html`), então nada precisa ser feito no Apache.

### 4.6 Verificação do servidor Web

🌐 **VM2**:

```bash
sudo ss -tlnp | grep apache
```

Esperado: as portas `80` e `443` em LISTEN.

🖥️ **PC**, com a VPN ligada:

```bash
curl -I http://192.168.1.8
curl -kI https://192.168.1.8
```

Esperado: `HTTP/1.1 200 OK` nos dois. O `-k` aceita o certificado autoassinado.

Dados do certificado:

```bash
openssl s_client -connect 192.168.1.8:443 </dev/null 2>/dev/null | openssl x509 -noout -subject -dates
```

Esperado: `CN = 192.168.1.8` e validade de 1 ano.

**No navegador**, abra `http://192.168.1.8` e `https://192.168.1.8`. No HTTPS aparece um aviso de segurança, que é normal com certificado autoassinado: clique em "Avançado → Aceitar o risco e continuar". Para ver o certificado, clique no **cadeado** e siga "Conexão não segura" → "Mais informações" → "Ver certificado".

---

## 5. Problemas encontrados e soluções

| Problema | Solução |
| --- | --- |
| O tutorial de VPN era para Debian e Ubuntu, e o PC usava Fedora | Instalar `NetworkManager-openvpn-gnome` com `dnf` e importar o perfil com `nmcli` |
| O `laboratorio.ovpn` abria como texto no navegador | Salvar o conteúdo como arquivo `laboratorio.ovpn` |
| Todo o tráfego de internet do PC passava pela VPN | `nmcli connection modify laboratorio ipv4.never-default yes` |
| Comandos colados com `#` no zsh rodaram fora da VM | Rodar um comando por vez, sem comentários, conferindo o prompt |
| A VM2 pegava hora da internet em vez da VM1 | Comentar as linhas `pool` e `sourcedir`, adicionar `server 192.168.1.7 iburst prefer` e reiniciar o Chrony |
| O `makestep` não corrigia o relógio alterado | Forçar uma nova medição com `sudo chronyc burst 4/4` antes do `makestep` |
| `curl: comando não encontrado` na VM2 | `sudo apt install -y curl` |
| Aviso `AH00558` no `configtest` | É inofensivo. Para eliminar, defina `ServerName` (seção 4.3) |
| `REMOTE HOST IDENTIFICATION HAS CHANGED` no SSH | `ssh-keygen -R IP_DA_VM` e conectar de novo |

---

## 6. Resumo rápido (checklist)

- [ ] VPN conectada (`ip -br a | grep tun0`)
- [ ] Senha trocada nas duas VMs (`passwd`)
- [ ] VM1: Chrony com NTP.br, `allow` para a VM2, `^*` em um servidor NTP.br
- [ ] VM2: Chrony só com a VM1 (`^* 192.168.1.7`), sem `pool` e sem `sourcedir`
- [ ] VM1: `chronyc clients` mostra a VM2
- [ ] VM2: teste `date -s` → `burst` → `makestep` corrige o relógio
- [ ] VM2: Apache nas portas 80 e 443 (`ss -tlnp`)
- [ ] `curl` retorna `200 OK` em HTTP e HTTPS a partir do PC
- [ ] Página com integrantes, VMs, relatório e trabalhos
- [ ] Relatório em PDF no servidor e no Campus Virtual
