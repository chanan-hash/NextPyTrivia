from socket import *

SERVER_IP = "0.0.0.0" # The server is listening to evey client, no matter if is from this computer or other
PORT = 8821
MAX_MSG_SIZE = 1024 # The max size of the message, to be coordinated
BIND_UDP = (SERVER_IP,PORT) # A tuple with the 'ip' and 'port'

server_socket = socket(AF_INET,SOCK_DGRAM) # DGRAM stands for UDP protocol
server_socket.bind(BIND_UDP)
print("Server up and running...")
# In contrast to the TCP protocol we don't need to use the methods 'liten()' or 'accept()', we can directly receive the message because of 'recvfrom'
(client_message,client_address) = server_socket.recvfrom(MAX_MSG_SIZE) # The method return tuple with  client's message\data he had send, and his IP address
# The client_address variable will help us to send back to the client a response, because we know now from where the message came from

data = client_message.decode()
print("The client sent: " + data)

response = "Super " + data
server_socket.sendto(response.encode(),client_address) # The method sendto, getting the data we want to send, and needs to be encoded. And then th client's IP address to know where to send it back

server_socket.close()

