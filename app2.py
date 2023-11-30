import threading
import socket
import uuid
import json
import os
import re

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
endereco = "127.0.0.1"
#port = input("Digite a porta: ")
port = 8108
#port2 = input("Digite a porta do destinatário: ")
port2 = 8102
#nick = input("Digite seu nome: ")
nick = "Trotsky"
server.bind((endereco, int(port)))

contatos = [("127.0.0.1", int(port2))]
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
                    for m in mensagens:
                        res_historico = json.dumps({"tag":"HISTORICO_TAG", "t":0, "id":m, "msg":mensagens[m]})
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
            elif pacote["tag"] == "HISTORICO_TAG":
                mensagens[pacote["id"]] = pacote["msg"]
            elif pacote["tag"] == "MSG_TAG":
                if relogio_logico[0] < int(pacote["t"]):
                    relogio_logico[0] = int(pacote["t"])
                    mensagens[pacote["id"]] = (f"{relogio_logico}{nicknames[end]}: {pacote['msg']}")
                elif relogio_logico[0] == int(pacote["t"]):
                    ultima_msg = mensagens.keys()[-1]
                    if ultima_msg > int(pacote["id"]):
                        relogio_logico[0] += 1
                        mensagens[pacote["id"]] = (f"{relogio_logico}{nicknames[end]}: {pacote['msg']}")
                    else:
                        mensagens[pacote["id"]] = (f"{relogio_logico}{nicknames[end]}: {pacote['msg']}")
                        re.sub(str(relogio_logico), "", mensagens[ultima_msg])
                        relogio_logico[0] += 1
                        mensagens[ultima_msg] = (f"{relogio_logico}{mensagens[ultima_msg]}")
                elif relogio_logico[0] > int(pacote["t"]):
                    relogio_logico[0] = int(pacote["t"])
                    id = uuid.uuid1()
                    mensagens[id] = "ERRO AO SINCRONIZAR MENSAGENS"
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