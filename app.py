# FAZER FUNCIONAMENTO NO SHELL
# TESTAR

import sys
import threading
import socket
import uuid
import json
import os
import re
import time
from cryptography.fernet import Fernet
#from dotenv import load_dotenv
import random

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
endereco = socket.gethostbyname(socket.gethostname())
#endereco = "192.168.0.103"
port = 8102
print(endereco, port)
abrir_chat = int(input("Serviço de mensagens Whatsapp 2\n[1]Conectar-se a um chat já estabelecido\n[2]Criar um novo chat\nEscolha:"))
if abrir_chat == 1:
    #port2 = input("Digite a porta do destinatário: ")
    port2 = 8102
    #end2 = input("Digite o endereco do destinatário: ")
    contatos = []
elif abrir_chat == 2:
    contatos = []

#load_dotenv()

k = "2cTg3PiAUzDTANGmlWM8qjpaGu2_E_h6ZLpvWr09gbE="
key = k.encode()
nick = input("Digite seu nome: ")
cipher_suite = Fernet(key)
server.bind((endereco, int(port)))

nicknames = {}
relogio_logico = [0]
mensagens = {}
id = uuid.uuid1()
buffer_env = {}

def ordena_msg(mensagens):
    mensagens = list(mensagens)
    l=len(mensagens)
    for i in range(l-1):
        for j in range(i+1,l):
            if mensagens[i][0]>mensagens[j][0]:
                t=mensagens[i]
                mensagens[i]=mensagens[j]
                mensagens[j]=t
    return mensagens

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
                # COMPARTILHA O HISTÓRICO DE MENSAGENS COM O MEMBRO DO CHAT QUE RETORNOU OU ACABA DE ENTRAR
                # ENVIANDO UMA POR UMA
                for m in mensagens:
                    res_historico = json.dumps({"tag":"HISTORICO_TAG", "t":0, "id":m, "msg":mensagens[m]})
                    send(res_historico)
                mensagens[pacote["id"]] = [relogio_logico[0]+1, f"Abre alas. {nicknames[end]} entrou na conversa!"]
                os.system('cls' if os.name == 'nt' else 'clear')
                ord_mensagens = ordena_msg(mensagens.values())
                for m in ord_mensagens:
                    print(f"[{m[0]}]{m[1]}")
                del(mensagens[pacote["id"]])
                # ENVIA SEU CONTATO E APELIDO PARA O NOVO MEMBRO
                id = uuid.uuid1()
                res_cont = json.dumps({"tag":"CONTATO_TAG", "t":0, "id":id.int, "msg":[endereco, int(port)], "nick":nick})
                send(res_cont)
                # ENVIA TODOS OS CONTATOS E APELIDOS QUE TEM REGISTRADO PARA O NOVO MEMBRO
                for c in contatos:
                    id = uuid.uuid1()
                    res_cont = json.dumps({"tag":"CONTATO_TAG", "t":0, "id":id.int, "msg":[c[0], c[1]], "nick":nicknames[c]})
                    send(res_cont)
            elif pacote["tag"] == "SYNC_TAG":
                for m in mensagens:
                    res_historico = json.dumps({"tag":"HISTORICO_TAG", "t":0, "id":m, "msg":mensagens[m]})
                    send(res_historico)
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
                relogio_logico[0] = pacote["msg"][0]
            elif pacote["tag"] == "ID_TAG":
                # ANALISA OS IDS ENVIADOS POR UM OUTRO NÓ
                ids = list(buffer_env.keys())
                for m in buffer_env.keys():
                    if m == pacote["msg"]:
                        ids.remove(m)
                for i in ids:
                    res_nack = json.dumps({"tag":"NACK_TAG", "id":i, "msg":buffer_env[i]})
                    send(res_nack)
            elif pacote["tag"] == "NACK_TAG":
                # RESPONDE A SOLICITAÇÃO DE UM NÓ O ENVIANDO UM NACK
                msg_crypto = cipher_suite.encrypt(mensagens[pacote["msg"][1]].encode())
                res = json.dumps({"tag":"MSG_NACK_TAG", "t":mensagens[pacote["msg"][0]], "id":pacote["id"], "msg":msg_crypto})
                sendto(res, end)
            elif pacote["tag"] == "MSG_NACK_TAG":
                # REGISTRA UMA MENSAGEM RECEBIDA ATRAVES DE SOLICITAÇÃO NACK
                msg_decrypto = cipher_suite.decrypt(pacote['msg'].encode())
                mensagens[pacote["id"]] = [pacote["t"], {msg_decrypto.decode('utf-8')}]
                ord_mensagens = ordena_msg(mensagens.values())
                for m in ord_mensagens:
                    print(f"[{m[0]}]{m[1]}")
            elif pacote["tag"] == "MSG_TAG":
                msg_decrypto = cipher_suite.decrypt(pacote['msg'].encode())
                if relogio_logico[0] < int(pacote["t"]):
                    relogio_logico[0] = int(pacote["t"])
                    mensagens[pacote["id"]] = [relogio_logico[0], f"{nicknames[end]}: {msg_decrypto.decode('utf-8')}"]
                elif relogio_logico[0] == int(pacote["t"]):
                    # CASO DUAS MENSAGENS TENHAM O MESMO TEMPO LÓGICO
                    # ELAS SÃO ORDENADAS ATRAVÉS DO ID
                    ultima_msg = mensagens.keys()[-1]
                    if ultima_msg > int(pacote["id"]):
                        relogio_logico[0] += 1
                        mensagens[pacote["id"]] = [relogio_logico[0], f"{nicknames[end]}: {msg_decrypto.decode('utf-8')}"]
                    else:
                        mensagens[pacote["id"]] = [relogio_logico[0], f"{nicknames[end]}: {msg_decrypto.decode('utf-8')}"]
                        relogio_logico[0] += 1
                        mensagens[ultima_msg][0] = relogio_logico[0]
                elif relogio_logico[0] > int(pacote["t"]):
                    relogio_logico[0] += 1
                    mensagens[pacote["id"]] = [relogio_logico[0], f"{nicknames[end]}: {msg_decrypto.decode('utf-8')}"]
                os.system('cls' if os.name == 'nt' else 'clear')
                ord_mensagens = ordena_msg(mensagens.values())
                for m in ord_mensagens:
                    print(f"[{m[0]}]{m[1]}")
        except:
            pass

def send(msg):
    for cliente in contatos:
        try:
            server.sendto(msg.encode('utf-8'), cliente)
        except:
            contatos.remove(cliente)

def sendto(msg, receptor):
    try:
        server.sendto(msg.encode('utf-8'), receptor)
    except:
        contatos.remove(receptor)

def envia_ids(cont):
    while cont < 30:
        cont += 1
        time.sleep(1)
    for m in mensagens:
        res = json.dumps({"tag":"ID_TAG", "msg":m})
    send(res)

t1 = threading.Thread(target=receive)
t1.start()

t2 = threading.Thread(target=envia_ids, args=([0]))
t2.start()

# ENVIA UMA MENSAGEM PARA O IP PELO QUAL ENTROU NO CHAT
# ANUNCIANDO SUA ENTRADA
id = uuid.uuid1()
res_entrou = json.dumps({"tag":"ENTROU_TAG", "t":0, "id":id.int, "msg":f"{nick}"})
send(res_entrou)

def envia(msg):
    msg_crypto = cipher_suite.encrypt(msg.encode())
    relogio_logico[0] += 1
    id = uuid.uuid1()
    res = json.dumps({"tag":"MSG_TAG", "t":relogio_logico[0], "id":id.int, "msg":msg_crypto.decode('utf-8')})
    mensagens[id.int] = [relogio_logico[0], f"{nick}: {msg}"]
    buffer_env[id.int] = [relogio_logico[0], f"{nick}: {msg}"]
    send(res)

def historico():
    ord_mensagens = ordena_msg(mensagens.values())
    for m in ord_mensagens:
        print(f"[{m[0]}]{m[1]}")

def sair():
    sys.quit()

sair_chat = False
while not sair_chat:
    msg = input()
    relogio_logico[0] += 1
    id = uuid.uuid1()
    msg_crypto = cipher_suite.encrypt(msg.encode())
    res = json.dumps({"tag":"MSG_TAG", "t":relogio_logico[0], "id":id.int, "msg":msg_crypto.decode('utf-8')})
    mensagens[id.int] = [relogio_logico[0], f"{nick}: {msg}"]
    buffer_env[id.int] = [relogio_logico[0], f"{nick}: {msg}"]
    os.system('cls' if os.name == 'nt' else 'clear')
    ord_mensagens = ordena_msg(mensagens.values())
    for m in ord_mensagens:
        print(f"[{m[0]}]{m[1]}")
    if msg == "!q":
        sair_chat = True
    else:
        send(res)