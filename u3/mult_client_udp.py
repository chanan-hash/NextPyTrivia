# A UPD protocol client that can send multiple message to the server till it ask to Exit, like a chat

import socket as sock

my_socket = sock.socket(sock.AF_INET,sock.SOCK_DGRAM)
SERVER_IP = "127.0.0.1"
PORT = 8821
MAX_MSG_SIZE = 1024

response = ""
while True:
    data = input("Please enter your message: ")
    my_socket.sendto(data.encode(),(SERVER_IP,PORT))
    (response, remote_address) = my_socket.recvfrom(MAX_MSG_SIZE)
    if response.decode() == "Quit":
        break
    print("The server sent: " + response.decode())

print("Bye!")
my_socket.close()