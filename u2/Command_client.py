from socket import *

my_sock = socket(AF_INET,SOCK_STREAM)
my_sock.connect(("127.0.0.1",8820))

data = ""
while data != "Bye":
    msg = input("Please Enter your command: \n")
    my_sock.send(msg.encode()) # sending the message to the server
    data = my_sock.recv(1024).decode() # getting the data form the server
    print("The server sent: " + data)

print("Closing the socket.")
my_sock.close()