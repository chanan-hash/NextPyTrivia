import time
import random
from socket import *

server_sock = socket(AF_INET, SOCK_STREAM)
server_sock.bind(("127.0.0.1",8820))
server_sock.listen()
print("server running...")

(client_sockt,client_address) = server_sock.accept()
print("Clients on!")

info = ""
while True:
    info = client_sockt.recv(1024).decode() # getting the data from the client. Now we can manipulate it

    print("Client sent: " + info)
    # Stop condition
    if info == "Quit":
        print("Closing the socket")
        client_sockt.send("Bye".encode())
        break

    res = info # need another variable to send back to the client, because if we'll send the 'info' he will get what he has sent

    if info == "NAME":
        res = "Yossi"
    elif info == "TIME":
        res =  time.ctime()
    elif info == "RAND":
        res = str(random.randint(1, 10))

    client_sockt.send(res.encode())

client_sockt.close()
server_sock.close()