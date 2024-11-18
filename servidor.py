#PONTIFICIA UNIVERSIDADE CATOLICA DO PARANÁ
#LUAN FELIX PIMENTEL
#ENGENHARIA DE SOFTWARE 2A

import socket as soco
import threading

# Lista de clientes conectados
lista_clientes = []

# Função para receber mensagens dos clientes
def receber_dados(conn, endereco):
    nome = conn.recv(50).decode()
    print(f"Conexão com sucesso com cliente {endereco}")
    print(f"{nome} entrou no chat!")

    # Adicionar o novo cliente na lista
    lista_clientes.append({'nome': nome, 'conexao': conn})

    # Enviar a mensagem de entrada do novo cliente para todos
    broadcast(f"{nome} entrou no chat!")

    while True:
        try:
            mensagem = conn.recv(1024).decode()
            print(f"{nome} >> {mensagem}")
            broadcast(f"{nome}: {mensagem}")
        except:
            index = lista_clientes.index({'nome': nome, 'conexao': conn})
            lista_clientes.remove(lista_clientes[index])
            conn.close()
            print(f"{nome} saiu do chat.")
            broadcast(f"{nome} saiu do chat.")
            return

# Função para enviar a mensagem para todos os clientes
def broadcast(mensagem):
    for cliente in lista_clientes:
        try:
            cliente['conexao'].sendall(mensagem.encode())
        except:
            index = lista_clientes.index(cliente)
            lista_clientes.remove(lista_clientes[index])
            cliente['conexao'].close()

# Configurações do servidor
HOST = 'localhost'
PORTA = 9999

# Criação do socket do servidor
socket_servidor = soco.socket(soco.AF_INET, soco.SOCK_STREAM)
socket_servidor.bind((HOST, PORTA))
socket_servidor.listen()
print(f"O servidor {HOST}:{PORTA} está aguardando conexões...")

while True:
    conn, ender = socket_servidor.accept()
    thread_cliente = threading.Thread(target=receber_dados, args=[conn, ender])
    thread_cliente.start()