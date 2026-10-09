import socket
import threading

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
PORTNUMBER = 5379 #todo custom
sock.bind(("0.0.0.0", 5379))
sock.listen()

clients={}

def handshake(sock):

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
    
    name = clientMessage[1][:-1]   #remove \n
    if name in clients:
        sock.sendall("IN-USE\n".encode())
        return

    sock.sendall(f"HELLO {name}\n".encode())
    clients[name]=sock
    listen(sock,name)
    del clients[name]

def listen(sock,user):

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
            sendMsg(clientRequest,user,sock)
        else:
            sock.sendall("BAD-RQST-HDR\n".encode())

def sendMsg(clientRequest,sender,senderSock):

    clientRequest = clientRequest.split(' ',2)  
    if len(clientRequest)!=3:
        senderSock.sendall("BAD-RQST-BODY\n".encode())
        return
    
    receiverName = clientRequest[1]
    if not (receiverName in clients):
        senderSock.sendall("UNKNOWN\n".encode())
        return

    msg = f"DELIVERY {sender} {clientRequest[2]}"
    receiverSock = clients[receiverName]
    receiverSock.sendall(msg.encode())
    senderSock.sendall("SEND-OK\n".encode())
    
def sendWho(sock):

    msg=""
    for name in clients:
        msg += name+","
    msg = msg[:-1]          #remove last comma
    sock.sendall(f"WHO-OK {msg}\n".encode())


def get_ip():
    s = None
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0)
        s.connect(('80.80.80.80', 1))
        return s.getsockname()[0]
    except OSError:
        return '127.0.0.1'
    finally:
        if s is not None:
            s.close()

print("server started\n")
print(f"ip:{get_ip()}\nport:{PORTNUMBER}")

while True:
    (tempsock, address) = sock.accept()
    print("debug print",sock.getsockname())
    if len(clients)>=64:
        tempsock.sendall("BUSY\n".encode())
        tempsock.shutdown(socket.SHUT_RDWR)
        tempsock.close()
    clientThread = threading.Thread(target=handshake, args=(tempsock,), daemon=True)
    clientThread.start()
