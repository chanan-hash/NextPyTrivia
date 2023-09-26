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

