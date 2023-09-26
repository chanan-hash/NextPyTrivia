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

def main:
    print("Setting up the server...")
    # Establishing sever socket
    server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server_socket.bind((SERVER_IP,SERVER_PORT))
    server_socket.listen() # listening for incoming connections
    print("listening for clients...")
    client_sockets = [] # For adding client sockets, in the beginning its empty because there's no connection

    while True: # While the socket is opem, we are scanning for finding clients
        ready_to_read, ready_to_write, in_error = select.select([server_socket] + client_socket, [], [])
        # In the beginning the list is not empty it contains the server's socket, that from it we can get new connections
        for current_socket in ready_to_read: # going through the socket list that we can read from
            if current_socket is server_socket: #  In every iteration we are checking the current socket is the server one, if it is we can establish connection, someone new wants to connect
                (client_socket, client_address) = current_socket.accept()
                print("New client joined! ", client_address)
                client_sockets.append(client_socket)
            else:
                pass

main()

