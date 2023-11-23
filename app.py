import threading
import socket
import uuid
import json

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
relogio_logico = 0

def receive():
    while True:
        try:
            data, end = server.recvfrom(1024) 
            msg = data.decode('utf-8')
            m = json.loads(msg)
            print(m)
            if msg.decode('utf-8').startswith("ENTROU_TAG"):
                nicknames[end] = msg.decode('utf-8')[11:]
                contatos.append(end)
                print(contatos)
                print(f"Abre alas. {nicknames[end]} entrou na conversa!")
                res_envia = json.dumps({relogio_logico, 0, f"ENVIA_TAG:{nick}"})
                send(res_envia)
            elif msg.decode('utf-8').startswith("ENVIA_TAG"):
                # ATUALIZA O USUÁRIO RECÉM CHEGADO COM OS NOMES
                # E ENDEREÇOS DOS USUÁRIOS ANTIGOS
                nicknames[end] = msg.decode('utf-8')[10:]
                if not end in contatos:
                    contatos.append(end)
            else:
                pacote = msg.decode('utf-8')
                t = int(pacote[0])
                if relogio_logico < t:
                    relogio_logico = t
                relogio_logico += 1
                print(f"({relogio_logico}){nicknames[end]}:{pacote[2]}")
        except:
            pass

def send(msg):
    for cliente in contatos:
        try:
            server.sendto(msg.encode('utf-8'), cliente)
        except:
            contatos.remove(cliente)

t1 = threading.Thread(target=receive)
t1.start()

res_entrou = json.dumps({relogio_logico, 0, f"ENTROU_TAG:{nick}"})
send(res_entrou)

sair_chat = False
while not sair_chat:
    msg = input()
    relogio_logico += 1
    id = uuid.uuid1()
    res = json.dumps({relogio_logico, id.int, msg})
    if msg == "!q":
        sair_chat = True
    else:
        send(res)