# FAZER ALGORITMO DE ORDENAÇÃO DE MENSAGENS
# TESTAR CONEXÃO 'INTERMEDIARIA'

import threading
import socket
import uuid
import json
import os
import re
import time
from cryptography.fernet import Fernet
#from dotenv import load_dotenv

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
endereco = "172.16.103.2"
port = 8102
abrir_chat = int(input("Serviço de mensagens Whatsapp 2\n[1]Conectar-se a um chat já estabelecido\n[2]Criar um novo chat\nEscolha:"))
if abrir_chat == 1:
    port2 = input("Digite a porta do destinatário: ")
    end2 = input("Digite o endereco do destinatário: ")
    contatos = [(end2, int(port2))]
    ult_digitos = int(input("Digite o código de confirmação: "))
elif abrir_chat == 2:
    contatos = []
    ult_digitos = port%100
    m = f"Bem vindo ao seu chat de mensagens! Seu código de confirmação é {ult_digitos}, compartilhe-o e compartilhe seu IP para que seus amigos possam se juntar ao chat!"

#load_dotenv()

k = ['E2rC93yv0nj5GKjeD_Jk1UK840OQAghVxzeUX7RQLQ0=', 'L-1OycKwouaVribCsG8jxNGc0b0z0wefZNv1I6qcUFY=', 'lX6t6L-ce-NzVtHEtNkzbausIsdzyBgK9Hjv_0jrQwM=', 'UJqY17Efsdncls9sNBN9iD-WmpjTFvceszR7uakMDi8=', 'sIq9CgPM8IiDYij1b_o_laafJz_wmqoXOKNkkYnwah8=', 'V6s4YlD65xGoAkHXkLnD-LWDCjM05vfQMBDi0tH9T1o=', 'fjIQj8iJeVmH7jCKmeO-2rft7dJjPhTQ59WedEuZCRo=', '5uskQnk3qgsM-dYgLv8WsJRaaDaqazqrb-T9_OJeiZc=', 'Sz3bs_nu-o4FbQZe6rp_uCRIo7unjGdu_6qkuSkdjBo=', 'yyHZNxDkNvEVddk4JMBpsrqp0B6NFll0jRW3k0orXrI=', 'N1iSU5PBmFmnC9svPnqmxtlVvdLCuQ22cZAQgg-4izc=', 'Fzro32WqCB_ahCBcZjgXi7zXuhPjuuqNH2dP3X_GaMg=', 'mRSeBQDkYmMMe9sFAJHDQREg3OlD3Sl00My8aATi4lA=', 'VChTDlGyr4i1SUbDTCLslJQXGukZ98ITpXhOmmm8uKM=', 'ZfUVXwLwUqaoSjJJjjjDjAisD7UwjdAyHJLV7yjz3LM=', '3fUu8d_bowt6Jl9V6awY-AJDIiVq1oWPNhGD16g5hpA=', 'KfDjob5HBRHbSloA29Is4IVm7MedJMO9-QyFOVvpQsk=', '0Gb8VYnpbjlFN5akRLY_CkPUHUvVeDUoAdgwgDzYP40=', 'UbaM3rv59m4n5ZSC1YC93HbxMIhySKh4sgPSdiWgdiY=', '5Hf08ahNvq2rqFu3R-CNHq439ZWeqoLgRiJT0NZH2bk=', '_U0xsDDi7KPzRmI4Ni0vR0mfvyJN1vwj_pkWkf4cop0=', 'I1GJ8_dwjK44_e2NmfwrK2lsOYwPnrW1OvoyHtwFK_Q=', 'x1tlq-3Y82CHXnHV0wMFQ4iPRU7Uw2q92rmQmx1PsaQ=', 'f-J_pLvt6vMePhSfqJOjXwO5NOnrWbY4Hnu3cmYuuz8=', 'J-mAzwcBM1-ug1cXDGhV1g-G0k4k2iPtDrZBIYtMCWA=', 'TmCjkXZpS2z8dCGOmTlgEkgCJPKeyIVoSEVtyswJeas=', 'oc70yKlwPKvW2S2N-PchNENn-34abXamXtI0avQRx5E=', '3id-elalw5XIyYQMPhZksSWHOGxpgKpL5tC7kGxFIP4=', 'wU-5EvKmYnfFs-8U98kOR5nir_Xzq49iDvg0TVL9T8Q=', 'KPQ9TYiTJWlSY3-l8Ne9nunt5w7GjC8eJ0tDKB8OLTY=', '_JJ-uk4H6ekX7o6E4aAF6Z2JrHFnfaAozmt1znOQEIE=', 'JItWIjAlj9BpJ6bL1jv36dYZ2KuK82iBFa10NPAnqos=', '126To6ZNuBqyNeEYc1i1yfui9leoDiQ4dlxpTW0ig2Q=', 'FMICmBU17r8K70_Jdj_gE-s-47FRlQW7_DT7DwNyrGg=', 'M5Fz2OgSD9tsi2eXAkODZjDXzkfpZzcWcWMw4WhTpBo=', 'IGv78p8DM4bCCdRf-lO07UaKgxgYKMHQvZOrnZgp_b4=', 'AdjPNJ35ZVbBO-7RG9UBIGfpeEF8NLoWHzCND8rDe-I=', '49s1NFE2nRQwJeftdUnlP3t6bAJ4WIZNly5eyFAeqiA=', 'MgnycEnxCG6zNzoIUtY2YnqtdBvdp_JRIdlykFnc-gY=', 'h8QL5_-zJNplsdWleBTm95AFeUDiutM3bg_josB1Rc4=', 'c1J35w1lLYdCmXed98JS0aqGAT7CYVKOpwyGU9pO3j4=', 'MSnMmlnWQWH0D-qL_2QX5hggTgw_GXrkHloer3bksog=', 'GEXE-NmOnxpT0Vu0wl8L2agyQh88jz0EEgbcBzPnapo=', 'Uwm3-OmF4cTeAHX86sessUq2hXkpBqy3Rb8D1MWFLX8=', 'BWAImWt61KqZ6Oeoy3Zg7HJlZ4Lcc2-tdT_KW2HilHs=', '3WZWqJTNt_9ZK6z5GjSS5FNj9A0kx40TctTWhIqsfRk=', 'vL0vODD_REq7sfjMTmgySuCkKdfwi-iMLzp8UDdzr2Q=', 'byfGymgwUwQS0V3wHF4kyOM6sAWrGqViHpqrNUYCcNs=', '-_kS-zKwlMiu2_ui_mjIH7Fr59gch-EzVk5b_t5LOCs=', '2q6SzLXgxu95FDHXQuAAvEapbC-bNz6Rh5P6ueG3dYE=', 'pN4iVNKJV7xn2i_H9Qcvj7SGVdTi0QHKvVo9thSrCYs=', 'wV8-nNiN5qcNuT3NrgcarcurkUJ_j1gs_XebDJkioTw=', 'PFhSSiQsM_KRjZ-C9lIxgJiPB9VCbsItkOrP1mQS_H0=', 'l8tIFIybU8qMrUf5m_CpLTqwUjWk13JirgRwRApYFo0=', '_uAgZYnIbxY-0C2vayy3xmJdpcvO-sCjkTJpR4HzhSQ=', 'w4ObamyE6g49tBlQ0C9jZpOrLzTrpWf7qvYiGf2_oDI=', 'S-1sBvhlrOVVe7Zc6-XdpnfJ2b1KrJj6LfgQRCkFJ2E=', 'MKrE4fxmicqeW3gDMzhzF4ZHTBMBKKr9NtkEy0JPdxU=', 'YnnBS2sHAUIbSjD41IWb0jIzEwI7t-66cxoLeuFuQVM=', 'aGd0O4jgXN6wYY1a3UdEzDagcfKcl2Psk2muZzzHCk4=', 'NqeF1mXRkM9ebLpLy-sHCYfyV-9Mr7DGf5obn5jXAbk=', 'lHt6J9gbhc_jiiq6jV-t_i0sahjhdHsj_8HcVMJoJ-o=', 'ppu_vUcGOtBndEs8Pwm9D_RFL4-9jjuZaV_xthTMFUY=', 'OB96g4fzsBWhQnC419GjHXHO3a-wpnAupzwuKWKkqd0=', 'gOphZOTnfP2og7lSy6bEhcKm0UZ5R5LiuKn2YBDXgSo=', 'Qv_68K0eaancsKr3YVx5vSpug1HqpQYooQDs5qHLVBs=', 'Ob5Tcf9HMgX47AIcxHpTVTIGD48lZmZ8RsoOfha4gVo=', 'fziwzQOXKzO_vGZ8se4ICG1PThLy1ltkextIsVBPKo0=', 'JjRXPgLEH1ebWrZcT8xr9mHnw4DbvZveAHKs8bui1ew=', '1fNZtStowQfxfzGVX3OrvYaDr8kgEzGMSQFlWqsRdtc=', 'tvN1GmZP0nmyxX1qj_N7xT28tlbzaH3TkbjI1CJomWg=', '4u8azoItOKaa0Hos3_I5_DnlZVOGx0d_V9590io596Y=', 'DvfU7_m7R3IL4XzEcHLv2C1pfqrA7vohgwxBexNGmBQ=', 'kX4sCu6dpkKDMrQnVAe8jvIZYfJa4kgYw6piS5kn2IM=', 'H2ARVt7SMs13y-NnU9KC12UfJfVaS5z9iqXfMrMT2Ho=', '2lGGkOSyE0PoCWU4XnqXXxoNattK8uSq71kCzuBUA6w=', '_hkq4XBKlrSRTuepKIB16UVsyM1c_vpZTZgkaC55yv0=', '3uMykvmL8N6nvesWgZzJntRGgTuiNWDC4r9yN0uwUlY=', 'bnNcUMnfIYnz-bQQyAF-pG2LytXD0pQhMqqYiZ91bKk=', 'jbY639CJf08m93VihsIW2GMl_xqKM8AchlzO6ZDAe_g=', '6KkLa1uN43CV43KyIDIrFayYfuXxBqU4xfrH3JWmr7A=', 'QphkHO7NMO4OVcq3nED9ik5FTtPe720N63EX7LCK5CU=', 'e0WKGoRz2lxifEWMW39p3dKJvf_zbsXgoMnmjL7J7nE=', 'hkhkO5I1zxt5y-m3javfLqFxS62CdzoyhRASsHBe5qs=', 'mW1o4Sr1TQfqO1GCNtGWGrRWB60jMwV4AxwucV84rQI=', 'NAzkYO9mPzt61rtLloRA_bQZMyR3Qkq3fqU82wabAhU=', 'e5PUwGULmAzxz8WNEtX2dCwivVD0Um9GfDTixKd2MZ8=', 'q4rfB2nyxMntmK-b_rpdotEIYJq49obH4IrqF3aap78=', 'FnJCFmqJlGZQdlx9R4BIrCW7IOq1mHFttt_sY2D6xXo=', 'j0cuXWDY2wNbOVatndiyuttcUNiG47JEKXgqu-frKKc=', 'wyCFohYK5yTRKR6XXqZmJEmrhH9lOIlIr_oSYWoZ9-Q=', 'ifnUBl2gTIzbJRv74Z6UQx-vkOSQqh8HJ42FPqM2CuI=', '4CY1toilYE8Hq46s5mWG-cCuurHbZi_S7eYZc7zpeMc=', 'PqsFI7BmIdO2aeBph-OiQ1pGXTx6FqtVCZ0FWGMO0hA=', 'JPyJD-pjD5CTHw_4uRgII9E3ADeYt8YiKqKiIx4b6cM=', 'F_UudCrqinO5zl1v7h1-nJ1400X31JpS28IDYVGUWUI=', 'CsbesIwegGYNEiMOkyNNFdb_taQ9c-Iws6mx9MzB9GE=', 'Xp3m1hAM-LGls1cLsWKo1evvZU4OJx98eQaNT0b7byY=', '2cTg3PiAUzDTANGmlWM8qjpaGu2_E_h6ZLpvWr09gbE=', 'GwNBlwW6fEOWKdSZaZ8kZZ-FlOJXuYAGVDwPpv7RIYk=']
key = k[ult_digitos]
#nick = input("Digite seu nome: ")
nick = "Trotsky"
cipher_suite = Fernet(key)
server.bind((endereco, int(port)))

nicknames = {}
relogio_logico = [0]
mensagens = {}
id = uuid.uuid1()
mensagens[id.int] = m

def ordena_msg(mensagens):
    l=len(mensagens)
    for i in range(l-1):
        for j in range(i+1,l):
            if mensagens[i][0]>mensagens[j][0]:
                t=mensagens[i]
                mensagens[i]=mensagens[j]
                mensagens[j]=t

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
                mensagens[pacote["id"]] = (f"Abre alas. {nicknames[end]} entrou na conversa!")
                os.system('cls' if os.name == 'nt' else 'clear')
                for m in mensagens:
                    print(mensagens[m])
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

def conta(cont):
    while cont < 180:
        cont += 1
        time.sleep(1)
    id = uuid.uuid1()
    res_sync = json.dumps({"tag":"SYNC_TAG", "t":0, "id":id.int, "msg":""})
    send(res_sync)

t1 = threading.Thread(target=receive)
t1.start()

t2 = threading.Thread(target=conta, args=([0]))
t2.start()

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