# This is a client for tcp (protocol) sever that  getting a message and returning it in Upper words

import socket
my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # using tcp protocol
my_socket.connect(("127.0.0.1" , 8820)) # connecting to the IP and port

my_socket.send("hello".encode())
data = my_socket.recv(1024).decode()
print("The server says: " + data)

my_socket.close()