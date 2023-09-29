from socket import *

my_socket = socket(AF_INET, SOCK_STREAM)

my_socket.connect(("127.0.0.1", 5555))

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
my_socket.close()
