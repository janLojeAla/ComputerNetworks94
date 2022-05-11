import socket
import threading
import re

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(("localhost", 5378))  #socket.gethostname()
sock.listen()

clients={}

def handshake(sock):
    clientMessage = sock.recv(16).decode("utf-8")
    while clientMessage[-1] != "\n" :
        clientMessage += sock.recv(16).decode("utf-8")
    clientMessage = clientMessage.split(' ')
    if len(clientMessage)==2:
        if clientMessage[0]=="HELLO-FROM":
            #send hi
            clients += {clientMessage[1],sock}
        else
            #send bad header
    elif
    #send bad message

while True:
    (tempsock, address) = sock.accept()
    clientThread = threading.Thread(target=handshake, args=(tempsock,), daemon=True)  # daemon makes it stop when main stops
    clientThread.start()


    
