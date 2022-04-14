import socket
import threading
import re
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def handShake(username):
	"""
	TODO: username can only have numbers and letters regex maybe?
	returns whether name is in use
	"""
	message = "HELLO-FROM {0}\n".format(username)
	string_bytes = message.encode("utf-8")
	sock.sendall(string_bytes)
	
	serverResponse = sock.recv(4096).decode('utf-8') #if we decode message at the start then we don't have to encode all the strings we are comparing it with
	if serverResponse=="HELLO {0}\n".format(username):
		return True
	elif serverResponse=="IN-USE\n":
		return False

def sendWho():
	message = "WHO\n"
	string_bytes = message.encode("utf-8")
	sock.sendall(string_bytes)

def sendMessage(command):
	command = command[1:].split(' ',1) #splits command at the 1st space
	#command.append('EMPTY MESSAGE')			   #if there is not message command[1] becomes ' ' creating a bad request body; otherwise this does basically nothing
	if len(command)<2:   #if no message after name
		print("Message cannot be empty")
	else:
		message = f"SEND {command[0]} {command[1]}\n"
		print("Message=",message)
		string_bytes = message.encode("utf-8")
		sock.sendall(string_bytes)

def listen():
	while True:
		#try:
			serverResponse = sock.recv(4096).decode("utf-8")
			if not serverResponse:
				return
			responseHead = serverResponse.split()[0]
			if responseHead == "WHO-OK":
				print("From Listen:",serverResponse) #TODO: diffrent stuff
			else:
				print("From Listen:",serverResponse) #TODO: diffrent stuff
		#except OSERROR:
			#pass


def main():
	
	host_port = ("143.47.184.219", 5378) #ip and port was in canvas discussion
	sock.connect(host_port)
	
	print("<Message explaining stuff>")
	hold_stuff = input("Name:")
	goodName = handShake(hold_stuff)
	while not goodName:   
		name = input("Someone already has that name:(\nOther name:")
		goodName = handShake(name)

	listenThread = threading.Thread(target=listen,daemon=True) #daemon makes it stop when main stops
	listenThread.start()

	finnish = False
	while not finnish:
		command = input()
		if command="": pass
		elif   command=="!quit": finnish=True
		elif command=="!who":  sendWho() 
		elif command[0]=="@": sendMessage(command)
		else: print("Invalid Command")

main()
