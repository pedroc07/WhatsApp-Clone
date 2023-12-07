# implementar timeout e confirmação de mensagens

import threading
import socket
import uuid
import json
import os
import re
from cryptography.fernet import Fernet
import base64

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
endereco = "172.16.103.1"
port = 8102
abrir_chat = int(input("Serviço de mensagens[1]Conectar-se a um chat já estabelecido\n[2]Criar um novo chat\nEscolha:"))
if abrir_chat == 1:
    port2 = input("Digite a porta do destinatário: ")
    end2 = input("Digite o endereco do destinatário: ")
    k = input("Digite a senha do chat: ")
    key = k.encode()
    contatos = [(end2, int(port2))]
elif abrir_chat == 2:
    key = Fernet.generate_key()
    contatos = []

#nick = input("Digite seu nome: ")
nick = "Bonaparte"
cipher_suite = Fernet(key)
server.bind((endereco, int(port)))

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
                # ENVIA O CONTATO DO NOVO MEMBRO PARA OS MEMBROS ANTIGOS
                id = uuid.uuid1()
                res_novo = json.dumps({"tag":"NOVO_TAG", "t":0, "id":id.int, "msg":end, "nick":pacote["msg"]})
                send(res_novo)
                nicknames[end] = pacote["msg"]
                if not end in contatos:
                    contatos.append(end)
                else:
                    # COMPARTILHA O HISTÓRICO DE MENSAGENS COM O MEMBRO DO CHAT QUE RETORNOU
                    # ENVIANDO UMA POR UMA
                    for m in mensagens:
                        res_historico = json.dumps({"tag":"HISTORICO_TAG", "t":0, "id":m, "msg":mensagens[m]})
                        send(res_historico)
                mensagens[pacote["id"]] = (f"Abre alas. {nicknames[end]} entrou na conversa!")
                os.system('cls' if os.name == 'nt' else 'clear')
                for m in mensagens:
                    print(mensagens[m])
                # ENVIA SEU CONTATO E APELIDO PARA O NOVO MEMBRO
                id = uuid.uuid1()
                res_cont = json.dumps({"tag":"CONTATO_TAG", "t":0, "id":id.int, "msg":[endereco, int(port)], "nick":nick})
                send(res_cont)
                # ENVIA TODOS OS CONTATOS E APELIDOS QUE TEM REGISTRADO PARA O NOVO MEMBRO
                for c in contatos:
                    id = uuid.uuid1()
                    res_cont = json.dumps({"tag":"CONTATO_TAG", "t":0, "id":id.int, "msg":[c[0], c[1]], "nick":nicknames[c]})
                    send(res_cont)
            elif pacote["tag"] == "CONTATO_TAG":
                # ATUALIZA O USUÁRIO RECÉM CHEGADO COM OS NOMES
                # E ENDEREÇOS DOS USUÁRIOS ANTIGOS
                n = (pacote["msg"][0], pacote["msg"][1])
                nicknames[n] = pacote["nick"]
                if not n in contatos:
                    contatos.append(n)
            elif pacote["tag"] == "NOVO_TAG":
                nicknames[pacote["msg"]] = pacote["nick"]
                if (not pacote["msg"] in contatos) and pacote["msg"] != endereco:
                    contatos.append(pacote["msg"])
            elif pacote["tag"] == "HISTORICO_TAG":
                mensagens[pacote["id"]] = pacote["msg"]
            elif pacote["tag"] == "MSG_TAG":
                if relogio_logico[0] < int(pacote["t"]):
                    relogio_logico[0] = int(pacote["t"])
                    msg_decrypto = cipher_suite.decrypt(pacote['msg'].encode())
                    mensagens[pacote["id"]] = (f"{relogio_logico}{nicknames[end]}: {msg_decrypto.decode('utf-8')}")
                elif relogio_logico[0] == int(pacote["t"]):
                    # CASO DUAS MENSAGENS TENHAM O MESMO TEMPO LÓGICO
                    # ELAS SÃO ORDENADAS ATRAVÉS DO ID
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

# ENVIA UMA MENSAGEM PARA O IP PELO QUAL ENTROU NO CHAT
# ANUNCIANDO SUA ENTRADA
id = uuid.uuid1()
res_entrou = json.dumps({"tag":"ENTROU_TAG", "t":0, "id":id.int, "msg":f"{nick}"})
send(res_entrou)

sair_chat = False
while not sair_chat:
    msg = input()
    relogio_logico[0] += 1
    id = uuid.uuid1()
    msg_crypto = cipher_suite.encrypt(msg.encode())
    res = json.dumps({"tag":"MSG_TAG", "t":relogio_logico[0], "id":id.int, "msg":msg_crypto.decode('utf-8')})
    mensagens[id.int] = (f"{relogio_logico}{nick}: {msg}")
    os.system('cls' if os.name == 'nt' else 'clear')
    for m in mensagens:
        print(mensagens[m])
    if msg == "!q":
        sair_chat = True
    else:
        send(res)