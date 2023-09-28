import threading
import queue
import socket

contatos = [("localhost", 8102)]

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
port = input("Digite a porta: ")
server.bind("localhost", int(port))

def receive():
    while True:
        try:
            msg, end = server.recvfrom(1024)
            print(msg.decode())
        except:
            pass

def send(msg):
    while True:
        for cliente in contatos:
            try:
                server.sendto(msg.encode(), cliente)
            except:
                contatos.remove(cliente)
                

while True:
    msg = input()
    server.send(msg)