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


my_server = socket(AF_INET, SOCK_DGRAM)
my_server.bind(SERVER_IP,PORT)

print("Server up and running...")
(client_message,client_address) = my_server.recvfrom(MAX_MSG_SIZE)


data = client_message.decode()
print("The client sent: " + data)


response = "Super " + data
special_sendto(my_server, response,client_address)

my_server.close()
