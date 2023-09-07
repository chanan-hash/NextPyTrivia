# This client is based on this videos:
# https://courses.campus.gov.il/courses/course-v1:CS+GOV_CS_networkpy103+2020_1/courseware/52a3378d07b4483eb4cdb15b899fd472/89de92924e64477fa43baac6a313e540/
# https://courses.campus.gov.il/courses/course-v1:CS+GOV_CS_networkpy103+2020_1/courseware/52a3378d07b4483eb4cdb15b899fd472/e3da5aa2ac79413cbdced241bdc32c18/?child=first

import socket

# we are creating an object that from socket type,
# socket.AF_INET --> defines that we are using IP protocol, the socket expecting to connect between 2 IP addresses
# SOCK_STREAM --> This argument defines using in TCP protocol that taking care of passing data behind the scenes
my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# now we'll connect it to the server
# my_socket.connect((IP,PORT)) ---> it getting an object, and inside the object we'll have the IP adr, and PORT
my_socket.connect(("127.0.0.1", 8820))  # 127.0.0.1 --> local host

data = ""
while data != "Bye": # while loop so the client can send to the server, till it ask to be closed
    msg = input("Please enter your message\n") # taking an input from the client
    # Sending a String to the server. The socket can transfer only binary data, so we're using the 'encode()' function to
    # convert it to binary sequence
    my_socket.send(msg.encode())
    data = my_socket.recv(1024).decode()  # recv - receive, getting back from the server response,
                                          # and decode() to convert it from binary to String.
                                          # recv(1024) --> 1024, is the max byte number we are asking to take out form the socket, we can take less than 1024 bytes, but not more.
    print("The server sent: " + data)

print("Closing client socket")
my_socket.close() # closing the socket

# To check the client side we'll use echo server, it will echo to the client the same data he sent

### When we are running client-server, always run the server before the client ###

