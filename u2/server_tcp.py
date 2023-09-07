from socket import  *

# Creating a new socket object
server_socket = socket(AF_INET,SOCK_STREAM) # IP protocol, and TCP protocol
server_socket.bind("0.0.0.0",8820) # connecting between the server we've created, to local IP and PORT, that are found on the server itself
                                            # getting a tuple with IP and PORT
                                            # IP - 0.0.0.0, means listen to everyone who addressing to your outside ip or everyone that address you from "local host"
                                            # listen to every request from inside the computer or outside

server_socket.listen() # ready to listen to clients
print("Server is up and running") # printing to the screen that everything is ready
(client_socket,client_address) = server_socket.accept() # approving the connection, the method waiting to a request from a client
print("Client connected")