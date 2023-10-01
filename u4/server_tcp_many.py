import socket, select

# 'select' function is scanning the whole time for a socket or a client to handle with
# 'select' --> is a Blocking function, means it stops the program running till it finishes to do whatever it needed
### --> ready_to_read, ready_to_write, in_error = select.select(read_list, write_list,_error_list)
# read_list - list of a sockets that we want to get info from
# write_list - sockets list that we may want to write to them
# error_list - sockets list that we may ant to know if an error occurred in them

### --> ready_to_read, ready_to_write, in_error = select.select([server_socket] + client_socket, [],[])
#for current_socket in ready_to_read:
    # Do something for every client

# The read_list is all the socket that are available,
# in the end "ready_to_read" --> will be a list of all the sockets that the server needs to handle

MAX_LENGTH_MSG = 1024
SERVER_PORT = 5555
SERVER_IP = "0.0.0.0"

def print_client_sockets(client_sockets: list): # printing the addresses of the connected sockets
    for c in client_sockets: # enumerate(client_sockets)
        print("\t", c.getpeername()) # this function is for getting the Ip and port of the client, and "\t" for Tab
        # We will call it evey time client has connected or disconnected

def main():
    print("Setting up the server...")
    # Establishing sever socket
    server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server_socket.bind((SERVER_IP,SERVER_PORT))
    server_socket.listen() # listening for incoming connections
    print("listening for clients...")
    client_sockets = [] # For adding client sockets, in the beginning its empty because there's no connection
    messages_to_send = [] # Answering to all the ready to write clients

    while True: # While the socket is opem, we are scanning for finding clients
        ready_to_read, ready_to_write, in_error = select.select([server_socket] + client_sockets, client_sockets, []) #The ready to write we've added the sockets list , our clients list we have, but not the server cause we don;t want to sent message to ourselves
        # In the beginning the list is not empty it contains the server's socket, that from it we can get new connections
        for current_socket in ready_to_read: # going through the socket list that we can read from
            if current_socket is server_socket: #  In every iteration we are checking the current socket is the server one, if it is we can establish connection, someone new wants to connect
                (client_socket, client_address) = current_socket.accept()
                print("New client joined! ", client_address)
                client_sockets.append(client_socket)
                print_client_sockets(client_sockets)
            else:
                print("New data from client!")
                data = current_socket.recv(MAX_LENGTH_MSG).decode() # 2 types of messages, or logout or regular message
                if data == "": # IN TCP, logout request is an empty String
                    print("Connection closed")
                    client_sockets.remove(current_socket) # removing it from the client list, and closing it
                    current_socket.close()
                    print_client_sockets(client_sockets)

                else: # This is a regular message, and because that is an echo server we will sed it the same message
                    print("Client sent: " + data)
                    # current_socket.send(data.encode())
                    messages_to_send.append((current_socket, data))

            # After we added all the clients tht are ready to read, we want to go over the sockets that ready to write to
            for message in messages_to_send:
                current_socket, data = message
                if current_socket in ready_to_write:
                    current_socket.send(data.encode())
                    messages_to_send.remove(message)


main()

