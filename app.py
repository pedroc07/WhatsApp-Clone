import threading
import socket
import uuid
import json

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
endereco = "127.0.0.1"
#port = input("Digite a porta: ")
port = 8102
#port2 = input("Digite a porta do destinatário: ")
port2 = 8108
#nick = input("Digite seu nome: ")
nick = "Bonaparte"
server.bind((endereco, int(port)))

contatos = []
nicknames = {}
relogio_logico = [0]

def receive():
    while True:
        try:
            data, end = server.recvfrom(1024) 
            p = data.decode('utf-8')
            pacote = json.loads(p)
            if pacote["msg"].startswith("ENTROU_TAG"):
                nicknames[end] = pacote["msg"][11:]
                contatos.append(end)
                print(contatos)
                print(f"Abre alas. {nicknames[end]} entrou na conversa!")
                res_envia = json.dumps({"t":0, "id":0, "msg":f"ENVIA_TAG:{nick}"})
                send(res_envia)
            elif pacote["msg"].startswith("ENVIA_TAG"):
                # ATUALIZA O USUÁRIO RECÉM CHEGADO COM OS NOMES
                # E ENDEREÇOS DOS USUÁRIOS ANTIGOS
                nicknames[end] = pacote["msg"][10:]
                if not end in contatos:
                    contatos.append(end)
            else:
                if relogio_logico[0] < int(pacote["t"]):
                    relogio_logico[0] = int(pacote["t"])
                else:
                    relogio_logico[0] += 1
                print(f"{relogio_logico}{nicknames[end]}:{pacote['msg']}")
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

res_entrou = json.dumps({"t":0, "id":1, "msg":f"ENTROU_TAG:{nick}"})
send(res_entrou)

sair_chat = False
while not sair_chat:
    msg = input()
    relogio_logico[0] += 1
    id = uuid.uuid1()
    res = json.dumps({"t":relogio_logico[0], "id":id.int, "msg":msg})
    if msg == "!q":
        sair_chat = True
    else:
        send(res)