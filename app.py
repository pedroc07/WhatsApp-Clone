import threading
import queue
import socket

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
port = input("Digite a porta: ")
port2 = input("Digite a porta do destinatário: ")
server.bind(("localhost", int(port)))

contatos = [("localhost", int(port2))]

def receive():
    while True:
        try:
            msg, end = server.recvfrom(1024)
            print(msg.decode())
        except:
            pass

def send(msg):
    for cliente in contatos:
        try:
            server.sendto(msg.encode(), cliente)
            print(f"Mensagem enviada a {cliente}")
        except:
            contatos.remove(cliente)

t1 = threading.Thread(target=receive)
t1.start()

while True:
    msg = input()
    send(msg)