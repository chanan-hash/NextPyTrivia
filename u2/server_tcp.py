# This server is based on this video
# https://courses.campus.gov.il/courses/course-v1:CS+GOV_CS_networkpy103+2020_1/courseware/52a3378d07b4483eb4cdb15b899fd472/e3da5aa2ac79413cbdced241bdc32c18/?child=first

from socket import  *

# Creating a new socket object
server_socket = socket(AF_INET,SOCK_STREAM) # IP protocol, and TCP protocol
server_socket.bind(("0.0.0.0",8820)) # Taking only One argument.
                                     # Connecting between the server we've created, to local IP and PORT, that are found on the server itself
                                     # getting a tuple with IP and PORT
                                     # IP - 0.0.0.0, means listen to everyone who addressing to your outside ip or everyone that address you from "local host"
                                     # listen to every request from inside the computer or outside

server_socket.listen() # ready to listen to clients
print("Server is up and running") # printing to the screen that everything is ready
(client_socket,client_address) = server_socket.accept() # approving the connection, the method waiting to a request from a client
print("Client connected") # This line of code will run, only if a client will connect to the server
                          # accept() --> returns a tuple, with 2 objects: 1. all the data that we need to communicate with the client. 2. IP and PORT that addressed to the server

while True: # while the client didn't ask to close the socket
    data = client_socket.recv(1024).decode() # getting the data from the client, and decoding it from bytes to String that we can understand
    print("Client sent: " + data)
    #client_socket.send(data.encode()) # sending back to the client a message as we've done in the client side, by encoding it
    if data == "Quit": # condition for closing the socket
        print("Closing client socket now...")
        client_socket.send("Bye".encode()) # Then the client will get a "Bey" message and will close the socket according to his condition (waiting for "Bye", look there)
        break # To jump out of the loop
    client_socket.send(data.encode())

client_socket.close() # closing the communication with the client on the client's object

# now we have 2 options: 1. going to listen mode and waiting to a new client, 2. or close the server's socket
server_socket.close()