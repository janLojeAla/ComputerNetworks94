import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host_port = ("143.47.184.219", 5378) #ip and port was in canvas discussion
sock.connect(host_port)

