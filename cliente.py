import socket as sock
import tkinter as tk
from tkinter import simpledialog
from PIL import Image, ImageTk
import threading

# Configurações do servidor
HOST = '192.168.99.103'
PORTA = 9999

# Criação do socket do cliente
try:
    cliente_socket = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
    cliente_socket.connect((HOST, PORTA))
except ConnectionRefusedError:
    print("Não foi possível conectar ao servidor.")
    exit()

# Janela para o usuário inserir seu nome
def solicitar_nome():
    janela_nome = tk.Tk()
    janela_nome.withdraw()  # Esconde a janela temporária
    nome_usuario = simpledialog.askstring("Nome de Usuário", "Digite seu nome para entrar no chat:")
    if not nome_usuario:
        print("Você precisa inserir um nome para continuar.")
        exit()
    return nome_usuario

nome_usuario = solicitar_nome()

# Interface do chat
janela = tk.Tk()
janela.title(f"Chat - {nome_usuario}")

# Adicionar imagem no topo
try:
    img = ImageTk.PhotoImage(Image.open("gui-sensei.jpg").resize((50, 50)))  # Redimensionar para 50x50
    label_imagem = tk.Label(janela, image=img)
    label_imagem.pack()
except Exception as e:
    print(f"Erro ao carregar a imagem: {e}")

# Lista de destinatários
frame_lista = tk.Frame(janela)
frame_lista.pack(side=tk.LEFT, padx=10, pady=10)
tk.Label(frame_lista, text="Destinatários").pack()
lista_destinatarios = tk.Listbox(frame_lista, height=10, width=20)
lista_destinatarios.insert(tk.END, "Todos")  # "Todos" é o padrão para broadcast
lista_destinatarios.pack()

# Caixa de entrada e botão de envio
frame_mensagem = tk.Frame(janela)
frame_mensagem.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)
caixa_entrada = tk.Entry(frame_mensagem, width=50)
caixa_entrada.pack(side=tk.LEFT, padx=5)
botao_enviar = tk.Button(frame_mensagem, text="Enviar", command=lambda: enviar_mensagem(nome_usuario))
botao_enviar.pack(side=tk.RIGHT, padx=5)

# Caixa de exibição de mensagens
frame_chat = tk.Frame(janela)
frame_chat.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
caixa_chat = tk.Text(frame_chat, state=tk.DISABLED, height=15, width=50)
caixa_chat.pack()

# Função para enviar mensagem (broadcast ou unicast)
def enviar_mensagem(usuario):
    mensagem = caixa_entrada.get()
    destinatario = lista_destinatarios.get(tk.ACTIVE)
    if destinatario == "Todos" or not destinatario:
        mensagem_final = f"BROADCAST:{usuario}:{mensagem}"
    else:
        mensagem_final = f"UNICAST:{usuario}:{destinatario}:{mensagem}"
    
    if mensagem:
        cliente_socket.send(mensagem_final.encode())
        caixa_entrada.delete(0, tk.END)

# Thread para receber mensagens
def receber_mensagens():
    while True:
        try:
            mensagem = cliente_socket.recv(1024).decode()
            caixa_chat.config(state=tk.NORMAL)
            caixa_chat.insert(tk.END, mensagem + "\n")
            caixa_chat.config(state=tk.DISABLED)
        except Exception as e:
            print(f"Erro ao receber mensagem: {e}")
            cliente_socket.close()
            break

# Iniciar thread de recepção de mensagens
thread_receber = threading.Thread(target=receber_mensagens, daemon=True)
thread_receber.start()

# Loop principal da interface
janela.mainloop()
