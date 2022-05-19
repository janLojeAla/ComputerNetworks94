import socket
import threading
import re

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(("localhost", 5378))  #socket.gethostname()
sock.listen()

clients={}

def handshake(sock):
    global clients
    clientMessage = sock.recv(16).decode("utf-8")
    while clientMessage[-1] != "\n" :
        clientMessage += sock.recv(16).decode("utf-8")
    clientMessage = clientMessage.split(' ')
    
    if not clientMessage:
        sock.sendall("BAD-RQST-HDR\n".encode())
        return
    if clientMessage[0]!="HELLO-FROM":
        sock.sendall("BAD-RQST-HDR\n".encode())
        return
    if len(clientMessage)!=2:
        sock.sendall("BAD-RQST-BODY\n".encode())
        return
    
    name = clientMessage[1][:-1]
    if name in clients:
        sock.sendall("IN-USE\n".encode())
        return

    sock.sendall(f"HELLO {name}\n".encode())
    clients[name]=sock
    listen(sock,name)
    del clients[name]


def listen(sock,user):
    global clients
    while True:
        clientRequest = sock.recv(16).decode("utf-8")
        if not clientRequest:
            return
        while clientRequest[-1] != "\n" :
            clientRequest += sock.recv(16).decode("utf-8")
        if not clientRequest:
            return

        print("clientRequest",clientRequest)
        responseHead = clientRequest.split(' ')[0]
        if responseHead == "WHO\n":
            sendWho(sock)
        elif responseHead == "SEND":
            if sendMsg(clientRequest,user):
                sock.sendall("SEND-OK\n".encode())
            else:
                sock.sendall("BAD-RQST-BODY\n".encode())
        else:
            sock.sendall("BAD-RQST-HDR\n".encode())

def sendMsg(clientRequest,sender):
    global clients
    clientRequest = clientRequest.split(' ',2)  
    if len(clientRequest)!=3:
        return False
    receiverName = clientRequest[1]
    if not (receiverName in clients):
        return False

    msg = f"DELIVERY {sender} {clientRequest[2]}"
    sock = clients[receiverName]
    sock.sendall(msg.encode())
    return True
    


def sendWho(sock):
    global clients
    msg=""
    for name in clients:
        msg += name+","
    msg = msg[:-1]          #remove last comma
    sock.sendall(f"WHO-OK {msg}\n".encode())



print("server started\n")
while True:
    (tempsock, address) = sock.accept()
    if len(clients)>=64:
        tempsock.sendall("BUSY\n".encode())
        tempsock.close()
    clientThread = threading.Thread(target=handshake, args=(tempsock,), daemon=True)
    clientThread.start()
