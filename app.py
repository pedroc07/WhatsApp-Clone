import threading
import socket

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
endereco = "localhost"
#port = input("Digite a porta: ")
port = 8102
#port2 = input("Digite a porta do destinatário: ")
port2 = 8101
#nick = input("Digite seu nome: ")
nick = "Bonaparte"
server.bind((endereco, int(port)))

contatos = [("localhost", int(port2))]
nicknames = {}

def receive():
    while True:
        try:
            msg, end = server.recvfrom(1024) 
            if msg.decode().startswith("ENTROU_TAG"):
                nicknames[end] = msg.decode()[11:]
                contatos.append(end)
                print(contatos)
                print(f"Abre alas. {nicknames[end]} entrou na conversa!")
                send(f"ENVIA_TAG:{nick}")
            elif msg.decode().startswith("ENVIA_TAG"):
                # ATUALIZA O USUÁRIO RECÉM CHEGADO COM OS NOMES
                # E ENDEREÇOS DOS USUÁRIOS ANTIGOS
                nicknames[end] = msg.decode()[10:]
                if not end in contatos:
                    contatos.append(end)
            else:
                print(f"{nicknames[end]}:{msg.decode()}")
        except:
            pass

def send(msg):
    for cliente in contatos:
        try:
            server.sendto(msg.encode(), cliente)
        except:
            contatos.remove(cliente)

t1 = threading.Thread(target=receive)
t1.start()

send(f"ENTROU_TAG:{nick}")

sair_chat = False
while not sair_chat:
    msg = input()
    if msg == "!q":
        sair_chat = True
    else:
        send(msg)