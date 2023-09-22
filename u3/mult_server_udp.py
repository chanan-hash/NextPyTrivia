from  socket import *

SERVER_IP = "0.0.0.0"
PORT = 8821
MAX_MSG_SIZE = 1024
BIND_UDP = (SERVER_IP,PORT)

server_socket = socket(AF_INET,SOCK_DGRAM)
server_socket.bind(BIND_UDP)
print("Server up and running...")

client_message = ""
while client_message != "Exit":
    (client_message, client_address) = server_socket.recvfrom(MAX_MSG_SIZE)
    data = client_message.decode()
    if data == "Exit":
        break
    print("The client sent: " + data)
    server_socket.sendto(data.encode(), client_address)

server_socket.sendto("Quit".encode(),client_address)
print("Server is closing")
server_socket.close()