# This is a server for tcp (protocol) sever that  getting a message and returning it in Upper words

import socket

server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_socket.bind(("127.0.0.1",8820))
server_socket.listen()
print("Server is ready and listening... ")

(client_sock , client_add) = server_socket.accept()
print("Client connected!")

data = client_sock.recv(1024).decode() # the moment we've got the data we can do stuff on it
msg = data.upper() # Making the word from client in capital letters
print("Client says: " + msg + "!!!")

client_sock.send((msg + "!!!").encode()) # sending back to the client what we've said
client_sock.close() # Client_sock represent a connection between a specific client
server_socket.close() # This represents the socket between server and client in general
