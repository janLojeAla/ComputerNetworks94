import socket
import threading

def handShake(username):

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host_port = ("143.47.184.219", 5378)  # ip and port was in canvas discussion
    sock.connect(host_port)

    message = "HELLO-FROM {0}\n".format(username)
    string_bytes = message.encode("utf-8")
    sock.sendall(string_bytes)
    serverResponse = sock.recv(4096).decode(
        'utf-8')  # if we decode message at the start then we don't have to encode all the strings we are comparing it with
    if serverResponse == "HELLO {0}\n".format(username):
        print("Login successful")
        return sock
    else:
        sock.close()
    if serverResponse == "IN-USE\n":
        print("Someone already has that name:(")
    elif serverResponse == "BUSY\n":
        print("The server is full, Probably a D-dos attack or something >:[")
    else:
        print("Just type a normal name. Y'know with LETTERS or NUMBERS")
    return None


def sendWho(sock):
    message = "WHO\n"
    string_bytes = message.encode("utf-8")
    sock.sendall(string_bytes)


def sendMessage(command, sock):
    command = command[1:].split(' ', 1)  # splits command at the 1st space
    if len(command) < 2:  # if no message after name
        print("Message cannot be empty")
    else:
        message = f"SEND {command[0]} {command[1]}\n"
        string_bytes = message.encode("utf-8")
        sock.sendall(string_bytes)


def listen(sock):
    while True:
        serverResponse = sock.recv(4096).decode("utf-8")
        if not serverResponse:
            return
        responseHead = serverResponse.split()[0]
        if responseHead == "WHO-OK":
            print("List of Users:", serverResponse.split()[1])
        elif responseHead == "DELIVERY":
            print("New Message From:", serverResponse.split()[1])
            print(serverResponse.split(' ', 2)[2])
        elif responseHead == "SEND-OK":
            print("Message Sent")
        elif responseHead == "UNKNOWN":
            print("Username currently unavailable")
        elif responseHead == "BAD-RQST-BODY":
            print("Error, please enter a valid message")
        elif responseHead == "BAD-RQST-HEADER":
            print("Error, please enter a valid message")
        else:
            print("Error,", serverResponse)


def main():
    username = input("Name:")
    sock = handShake(username)
    while not sock:
        name = input("Other name:")
        sock = handShake(name)

    listenThread = threading.Thread(target=listen, args=(sock,), daemon=True)  # daemon makes it stop when main stops
    listenThread.start()

    finish = False
    while not finish:
        command = input()
        if command == "":
            pass
        elif command == "!quit":
            finish = True
        elif command == "!who":
            sendWho(sock)
        elif command[0] == "@":
            sendMessage(command, sock)
        else:
            print("Invalid Command")


main()

