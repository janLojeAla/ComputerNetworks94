import socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)



def login(username):
	"""
	returns problem
	returns None if no problem
	"""
	message = "HELLO-FROM {0}\n".format(username)
	string_bytes = message.encode("utf-8")
	sock.sendall(string_bytes)
	
	"HELLO <name>\n"
	serverResponse = sock.recv(4096)
	print(serverResponse)
	if not serverResponse:
		return "Socket is closed";
	elif serverResponse=="HELLO {0}\n".format(username).encode("utf-8"):
		return ""
	elif serverResponse=="IN-USE\n".encode("utf-8"):
		return "User name taken"
	else:
		return "Invalid Server Response"

host_port = ("143.47.184.219", 5378) #ip and port was in canvas discussion
sock.connect(host_port)

print(login("joe"))
