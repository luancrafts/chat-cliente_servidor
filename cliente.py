#PONTIFICIA UNIVERSIDADE CATOLICA DO PARANÁ
#LUAN FELIX PIMENTEL
#ENGENHARIA DE SOFTWARE 2A

import socket as sock
import tkinter as tk

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

# Criação da interface gráfica
janela = tk.Tk()
janela.title("Chat - Gui-sensei")
# Tamanho da janela que aparece a foto do gui, campo textual e botão de enviar
janela.geometry("400x300")  

# Caixa de mensagens
caixa_mensagens = tk.Text(janela, height=10, width=50, state=tk.DISABLED, wrap=tk.WORD)
caixa_mensagens.grid(row=0, column=0, padx=10, pady=10)

# Caixa de entrada de mensagem
caixa_entrada = tk.Entry(janela, width=50)
caixa_entrada.grid(row=1, column=0, padx=10, pady=10)

# Função para enviar mensagem
def enviar_mensagem():
    mensagem = caixa_entrada.get()
    if mensagem:
        cliente_socket.sendall(mensagem.encode())
        caixa_mensagens.config(state=tk.NORMAL)
        caixa_mensagens.insert(tk.END, f"Você: {mensagem}\n")
        caixa_mensagens.config(state=tk.DISABLED)
        caixa_entrada.delete(0, tk.END)

# Botão de envio
botao_enviar = tk.Button(janela, text="Enviar", command=enviar_mensagem)
botao_enviar.grid(row=2, column=0, padx=10, pady=10)

# Iniciar o loop da interface gráfica
janela.mainloop()
