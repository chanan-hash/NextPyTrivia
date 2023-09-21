# This is a client for UDP transfer protocol

import socket
# The second argument the is passing by the function that creating the socket represent the protocol
my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Here in UDP we are using something else, instead of SOCK_STREAM, we are using SOCK_DGRAM to say we are using UDP protocol

SERVER_IP = "127.0.0.1"
PORT = 8821

MAX_MSG_SIZE = 1024

# now we can send immediately the message
my_socket.sendto("geeks".encode(),(SERVER_IP,PORT))
# Because there is no permanent link/connection ti the server so we aren't using the function 'connect' like in TCP
# Every message we have, we can send it by the method 'sendto'

# In TCP creates socket in front of the server and keeps it open the whole time they are speaking
# In UDP very message stand by itself, and there's no socket that stays open in front of the server

(response, remote_address) = my_socket.recvfrom(MAX_MSG_SIZE)
# In TCP, the socket binds\connects permanently between both side, so we know from where the message cam from
# In UDP, it doesn't happen so we need to know from where we've got the message
# the method 'recvfrom' - returns tuple that is build from 2 arguments --> 1. the message, 2. the IP address of the server\sender

data = response.decode() # like in TCP, decoding the message and printing it
print("The server sent: " + data)

my_socket.close() # Closing the connection, like in TCP