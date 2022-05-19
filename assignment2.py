import socket
import threading
import re

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(("localhost", 5378))  #socket.gethostname()
sock.listen()

clients={}

def handshake(sock):    #TODO:check for repeated name
    global clients
    clientMessage = sock.recv(16).decode("utf-8")
    while clientMessage[-1] != "\n" :
        clientMessage += sock.recv(16).decode("utf-8")
    clientMessage = clientMessage.split(' ')
    
    if not clientMessage:
        #send bad header
        return
    if clientMessage[0]!="HELLO-FROM":
        #send bad header
        return
    if len(clientMessage)!=2:
        #send bad-body
        return
    name = clientMessage[1]  #technically the name variable holds name and line change but like meh
    sock.sendall(f"HELLO {name}".encode())
    clients[clientMessage[1]]=sock
    listen(sock,name[:-1])
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
        responseHead = clientRequest.split()[0] #split on white space removes "\n"
        if responseHead == "WHO":
            sendWho(sock)
        elif responseHead == "SEND":
            if sendMsg(clientRequest,user):
                pass #send OK
            else:
                pass #bad rqst body
        else:
            pass #send bad header

def sendMsg(clientRequest,sender):
    global clients
    clientRequest = clientRequest.split(' ',2)  
    if len(clientRequest)!=3:
        return False
    receiverName = clientRequest[1]
    if not (receiverName+'\n' in clients):
        return False

    msg = f"DELIVERY {sender} {clientRequest[2]}"
    sock = clients[receiverName+'\n']
    sock.sendall(msg.encode())
    


def sendWho(sock):
    global clients
    msg=""
    for name in clients:
        msg += name[:-1]+","  #-1 to remove \n
    msg = msg[:-1]
    sock.sendall(f"WHO-OK {msg}\n".encode())



print("server started\n")
while True:
    (tempsock, address) = sock.accept()
    clientThread = threading.Thread(target=handshake, args=(tempsock,), daemon=True)
    clientThread.start()
    
