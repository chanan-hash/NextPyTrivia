from random import *
from socket import *

def special_sendto(socket_object: socket, response, client_address):
    fail = random.randint(1, 3)
    if not (fail == 1):
        socket_object.sendto(response.encode(), client_address)
    else:
        print("Oops")

SERVER_IP = "0.0.0.0"
PORT = 8821
MAX_MSG_SIZE = 1024

my_socket = socket(AF_INET,SOCK_DGRAM)
packet = "hello"
special_sendto(my_socket, packet ,(SERVER_IP,PORT))

(response, remote_address) = my_socket.recvfrom(MAX_MSG_SIZE)
data = response.decode()
print("The server sent: ", data)

my_socket.close()