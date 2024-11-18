#PONTIFICIA UNIVERSIDADE CATOLICA DO PARANA
#LUAN FELIX PIMENTEL

#Foi utilizado TCP e não UDP, o broadcast foi apenas simulado com listas (UDP poderia perder mensagem e mais complexo)
#percebi que exige mais processamento do servidor
#Entrega confiável das mensagens
#Ordem correta dos pacotes
#Verificação de erros
#Controle de fluxo
#Cadas mensagem é uma conexão TCP individual


# Importação de bibliotecas
import socket as soco
import threading

# Configurações do servidor, nesse caso coloquei o IP da rede que estava conectado
HOST = '192.168.99.103'
PORTA = 9999

# Lista de clientes conectados
lista_clientes = []

# Função para notificar a saída de um cliente
def notificar_saida(nome_cliente):
    mensagem = f"NOTIFICAÇÃO: {nome_cliente} saiu do chat."
    for cliente in lista_clientes:
        try:
            #acesso a conexão em cliente[conexao]
            #Nesse caso a função faz o envio para todos que fulaninho saiu do chat
            cliente['conexao'].sendall(mensagem.encode('utf-8'))
        except:
            continue

# só envia a lista de participantes para todos os clientes
def enviar_lista_participantes():
    #cria uma lista nova so com o nome de quem ta ativo
    nomes = [cliente['nome'] for cliente in lista_clientes]
    #join concatena os nomes com virgulas pra exibir a mensagem
    mensagem = "PARTICIPANTES:" + ",".join(nomes)
    for cliente in lista_clientes:
        try:
            cliente['conexao'].sendall(mensagem.encode())
        except:
            #remove o cliente que deu erro se deu algo bo
            remover_cliente(cliente['conexao'])

# Função para remover cliente da lista de clientes conectados
def remover_cliente(conn):
    #aqui recebo a conexão do cliente que é pra ser removido
    #retorna pares de indice e cliente
    #procura na lista de clientes comparando conexões retorna i quando encontra
    index = next((i for i, c in enumerate(lista_clientes) if c['conexao'] == conn), None)
    if index is not None:
        lista_clientes.pop(index)
    conn.close()

# Função para interpretar e enviar mensagens
def enviar_mensagem(mensagem, remetente):
    #foi usado o /unicast como pratica pra separar a mensagem a ser enviada e não fazer broadcast
    if '/unicast' in mensagem:
        #divide a mensagem com split
        #o formato da mensagem sempre é /unicast nomedapessoa mensagem a ser enviada
        partes = mensagem.split(maxsplit=2)
        # Mensagem unicast no formato "/unicast destinatario mensagem"
        print(partes)
        destinatario = partes[1]
        conteudo = partes[2]
        unicast(f"[Privado] {conteudo}", destinatario, remetente)
    else:
        # Mensagem de broadcast
        broadcast(mensagem, remetente)

# Função para enviar mensagem a todos (broadcast)
def broadcast(mensagem, remetente=None):
    for cliente in lista_clientes:
        #if cliente['conexao'] != remetente:  # Não reenviar para o remetente
            try:
                cliente['conexao'].sendall(mensagem.encode())
            except:
                remover_cliente(cliente['conexao'])

# Função para enviar mensagem a um cliente específico (unicast)
def unicast(mensagem, destinatario, remetente=None):
    for cliente in lista_clientes:
        print(cliente)
        #Procura na lista o cliente com o nome igual ao destinatário
        if cliente['nome'] == destinatario:
            try:
                cliente['conexao'].sendall(mensagem.encode())
            except:
                remover_cliente(cliente['conexao'])
            break

# Função para gerenciar mensagens de um cliente
def receber_dados(conn, endereco):
    try:
        # Receber o nome do cliente
        nome = conn.recv(1024).decode()
        print(f"Conexão estabelecida com {endereco} ({nome})")
        lista_clientes.append({'nome': nome, 'conexao': conn})

        # Notificar os demais clientes e enviar a lista de participantes
        broadcast(f"{nome} entrou no chat!", conn)
        enviar_lista_participantes()

        # Receber mensagens continuamente
        while True:
            mensagem = conn.recv(1024).decode()
            enviar_mensagem(mensagem, conn)
    except:
        # Tratamento ao cliente desconectar
        print(f"Cliente {nome} ({endereco}) desconectado.")
        remover_cliente(conn)
        broadcast(f"{nome} saiu do chat!")
        enviar_lista_participantes()

# Criação do socket do servidor
#TCP/IP
socket_servidor = soco.socket(soco.AF_INET, soco.SOCK_STREAM)
#Liga o socket as portas especificadas
socket_servidor.bind((HOST, PORTA))
#escuta por conexões
socket_servidor.listen()
print(f"O servidor está rodando em {HOST}:{PORTA}...")

# Loop infinito para aceitar conexões
while True:
    conn, endereco = socket_servidor.accept()
    #executa a função de receber dados
    thread_cliente = threading.Thread(target=receber_dados, args=(conn, endereco))
    thread_cliente.start()
