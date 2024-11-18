#PONTIFICIA UNIVERSIDADE CATOLICA DO PARANÁ
#LUAN FELIX PIMENTEL
#ENGENHARIA DE SOFTWARE 2A

import socket as sock
import tkinter as tk
import threading

# Configurações do servidor
HOST = 'localhost'
PORTA = 9999

# Criação do socket do cliente
try:
    cliente_socket = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
    cliente_socket.connect((HOST, PORTA))
except ConnectionRefusedError:
    print("Não foi possível conectar ao servidor.")
    exit()

# Função para enviar mensagem (broadcast ou unicast)
def enviar_mensagem():
    mensagem = caixa_entrada.get()
    destinatario = lista_destinatarios.get(tk.ACTIVE)
    
    # Verifica se é uma mensagem de broadcast ou unicast
    if destinatario == "Todos" or destinatario == "":
        # Broadcast para todos os clientes
        mensagem_final = f"BROADCAST:{mensagem}"
    else:
        # Unicast para um destinatário específico
        mensagem_final = f"UNICAST:{destinatario}:{mensagem}"
    
    if mensagem:
        cliente_socket.sendall(mensagem_final.encode())
        caixa_mensagens.config(state=tk.NORMAL)
        caixa_mensagens.insert(tk.END, f"Você para {destinatario if destinatario else 'Todos'}: {mensagem}\n")
        caixa_mensagens.config(state=tk.DISABLED)
        caixa_entrada.delete(0, tk.END)

# Função para atualizar a lista de destinatários
def atualizar_destinatarios(usuarios):
    """
    Atualiza a lista de usuários conectados na interface.
    """
    lista_destinatarios.delete(0, tk.END)
    lista_destinatarios.insert(tk.END, "Todos")  # Opção para broadcast
    for usuario in usuarios:
        lista_destinatarios.insert(tk.END, usuario)

# Função para escutar mensagens do servidor
def escutar_servidor():
    while True:
        try:
            mensagem = cliente_socket.recv(1024).decode('utf-8')
            
            # Verifica se a mensagem é a lista de usuários conectados
            if mensagem.startswith("USERS:"):
                usuarios = mensagem.replace("USERS:", "").split(',')
                atualizar_destinatarios(usuarios)
            else:
                # Exibe a mensagem recebida no chat
                caixa_mensagens.config(state=tk.NORMAL)
                caixa_mensagens.insert(tk.END, f"{mensagem}\n")
                caixa_mensagens.config(state=tk.DISABLED)
        except:
            print("Erro na conexão com o servidor.")
            cliente_socket.close()
            break

# Criação da interface gráfica
janela = tk.Tk()
janela.title("Chat - Gui-sensei")
janela.geometry("400x400")

# Caixa de mensagens
caixa_mensagens = tk.Text(janela, height=10, width=50, state=tk.DISABLED, wrap=tk.WORD)
caixa_mensagens.grid(row=0, column=0, padx=10, pady=10, columnspan=2)

# Caixa de entrada de mensagem
caixa_entrada = tk.Entry(janela, width=40)
caixa_entrada.grid(row=1, column=0, padx=10, pady=10)

# Lista de destinatários (para unicast)
lista_destinatarios = tk.Listbox(janela, height=5, selectmode=tk.SINGLE)
lista_destinatarios.grid(row=1, column=1, padx=10, pady=10)
lista_destinatarios.insert(tk.END, "Todos")  # Adiciona opção para broadcast

# Botão de envio
botao_enviar = tk.Button(janela, text="Enviar", command=enviar_mensagem)
botao_enviar.grid(row=2, column=0, padx=10, pady=10, columnspan=2)

# Iniciar thread para escutar mensagens do servidor
receber_thread = threading.Thread(target=escutar_servidor)
receber_thread.daemon = True
receber_thread.start()

# Iniciar o loop da interface gráfica
janela.mainloop()