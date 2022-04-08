import socket
import threading
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def handShake(username):
	"""
	returns problem
	returns whether name is in use
	"""
	message = "HELLO-FROM {0}\n".format(username)
	string_bytes = message.encode("utf-8")
	sock.sendall(string_bytes)
	serverResponse = sock.recv(4096)
	print(serverResponse)
	if serverResponse=="HELLO {0}\n".format(username).encode("utf-8"): #server messages come encoded in utf-8
		return False
	elif serverResponse=="IN-USE\n".encode("utf-8"):
		return True

def who():
	pass

def message(command):
	pass


def main():
	host_port = ("143.47.184.219", 5378) #ip and port was in canvas discussion
	sock.connect(host_port)
	
	print("<Message explaining stuff>")
	name = input("Name:")
	nameInUse = handShake(name)
	while nameInUse:
		input("Someone already has that name:(\nOther name:")
		nameInUse = handShake(name)

	# TODO:Start thread here that listens for messages
	# from other users, and displays them
	
	quit=False
	while not quit:
		command = input()
		if   command=="!quit": quit = True
		elif command=="!who":  who() #temporary, who function is empty
		elif command[0]=="@":  message(command) #temporary 
		else: print("Invalid Command")
main()
