import socket

def main() :
	server_IP   = "192.168.0.7" # this computer
	server_PORT = 8080 # the port that the wemos should connect to

	server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

	server_sock.bind((server_IP, server_PORT))
	server_sock.listen(3)
	print("here")
	client_sock, addr = server_sock.accept()

	while True:
		try :
			data, addr = client_sock.recvfrom(128) # buffer size is 1024 bytes
			print "received message:", data
			client_sock.sendto("ab\n".encode(), ("192.168.0.7", 8080))
		except KeyboardInterrupt :
			print("socket close")
			client_sock.close()
			server_sock.close()
			break
		else :
			pass

if __name__=="__main__" :
	main()
