from socket import *

my_socket = socket(AF_INET, SOCK_STREAM)
my_socket.connect(("127.0.0.1" , 5555)) # connecting to the IP and port

while True:
    data = my_socket.recv(1024).decode()

my_socket.close()
