# fazer ordenação
# ver criptogrfia
# enviar historico de mensagens

import threading
import socket
import uuid
import json
import os

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
mensagens = {}

def receive():
    while True:
        try:
            data, end = server.recvfrom(1024) 
            p = data.decode('utf-8')
            pacote = json.loads(p)
            if pacote["tag"] == "ENTROU_TAG":
                nicknames[end] = pacote["msg"]
                if not end in contatos:
                    contatos.append(end)
                else:
                    id = uuid.uuid1()
                    res_historico = json.dumps({"tag":"HISTORICO_TAG", "t":0, "id":id.int, "msg":mensagens})
                    send(res_historico)
                mensagens[pacote["id"]] = (f"Abre alas. {nicknames[end]} entrou na conversa!")
                os.system('cls' if os.name == 'nt' else 'clear')
                for m in mensagens:
                    print(mensagens[m])
                id = uuid.uuid1()
                res_envia = json.dumps({"tag":"ENVIA_TAG", "t":0, "id":id.int, "msg":f"{nick}"})
                send(res_envia)
            elif pacote["tag"] == "ENVIA_TAG":
                # ATUALIZA O USUÁRIO RECÉM CHEGADO COM OS NOMES
                # E ENDEREÇOS DOS USUÁRIOS ANTIGOS
                nicknames[end] = pacote["msg"]
                if not end in contatos:
                    contatos.append(end)
            elif pacote["tag"] == "MSG_TAG":
                if relogio_logico[0] < int(pacote["t"]):
                    relogio_logico[0] = int(pacote["t"])
                else:
                    relogio_logico[0] += 1
                mensagens[pacote["id"]] = (f"{relogio_logico}{nicknames[end]}: {pacote['msg']}")
                os.system('cls' if os.name == 'nt' else 'clear')
                for m in mensagens:
                    print(mensagens[m])
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

id = uuid.uuid1()
res_entrou = json.dumps({"tag":"ENTROU_TAG", "t":0, "id":id.int, "msg":f"{nick}"})
send(res_entrou)

sair_chat = False
while not sair_chat:
    msg = input()
    relogio_logico[0] += 1
    id = uuid.uuid1()
    res = json.dumps({"tag":"MSG_TAG", "t":relogio_logico[0], "id":id.int, "msg":msg})
    mensagens[id.int] = (f"{relogio_logico}{nick}: {msg}")
    os.system('cls' if os.name == 'nt' else 'clear')
    for m in mensagens:
        print(mensagens[m])
    if msg == "!q":
        sair_chat = True
    else:
        send(res)