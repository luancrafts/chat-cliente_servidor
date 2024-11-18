# Aplicativo de Chat

Saudações, caríssimos iniciantes na arte das comunicações wiccanas!

Abaixo, vocês encontrarão um pequeno guia para dominar este **feitiço de interação conhecido como Aplicativo de Chat**—uma criação surpreendentemente fácil de conjurar, mas poderosa o suficiente para unir mentes distantes. Tudo isso com a graça dos encantamentos Python e das bibliotecas `socket` e `Tkinter`. Sigam atentamente e logo estarão trocando mensagens como bruxos experientes!

---

## O Ritual de Invocação

1. Primeiramente, lancem o script `servidor.py` em um terminal. Este ato trará o servidor à vida, permitindo que ele receba conexões de qualquer alma que se aventure em nossa rede.

2. Em seguida, execute o script `cliente.py` em outro terminal (pois é sempre prudente manter um certo distanciamento entre os espíritos digitais!). Este passo abrirá o portal do cliente, conectando-o ao servidor central.

3. Com o cliente em mãos, digite seu feitiço (ou melhor, sua mensagem) no campo de entrada e clique em "Enviar". As palavras enviadas tanto por você quanto por outros colegas aparecerão magicamente na caixa de chat.

4. Deseja ainda mais vozes pro coro de DOWN DOWN DOWN THE ROAD DOWN THE WITCHES ROAD em seu encantamento coletivo? Basta rodar o `cliente.py` em quantos terminais desejar, cada um trazendo um novo participante à sua comunhão digital!

---

## Como o código está dividido:

A aplicação está dividida em dois feitiços principais, cada um com sua função mágica:

1. **Servidor (`servidor.py`):**
   - O servidor gerencia as conexões e realiza o encantamento de transmissão das mensagens entre os clientes.
   - Graças ao módulo `threading`, ele recebe múltiplas conexões simultaneamente, quase como um verdadeiro mestre das poções multitarefas.
   - A função `broadcast()` é o feitiço que entrega as mensagens aos clientes conectados, mantendo todos cientes das palavras uns dos outros.

2. **Cliente (`cliente.py`):**
   - O cliente possui uma GUI encantada com o auxílio do Tkinter, incluindo uma imagem mística do Gui-sensei, mestre dessa prática.
   - Há também uma caixa de chat, onde as mensagens aparecem, um campo de entrada para que você possa formular seus feitiços verbais e o botão "Enviar" que, ao ser pressionado, dispara a mensagem direto para o servidor.

---

## Ingredientes Essenciais

- **Python** 3.x
- **Módulo `socket`** para conexão
- **Módulo `threading`** para controle dos clientes
- **Módulo `tkinter`** para a interface mágica
- **Módulo `PIL`** (ou Pillow), a Biblioteca de Imagens, para retratar nosso caro Gui-sensei

---

## Instruções para Evocação

1. Faça o download do repositório ou obtenha os scripts `cliente.py` e `servidor.py`.
2. Certifique-se de que as dependências estão instaladas, lançando o seguinte comando:
   ```bash
   pip install pillow
