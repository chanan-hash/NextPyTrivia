import socket
import chatlib  # To use chatlib functions or consts, use chatlib.****

SERVER_IP = "127.0.0.1"  # Our server will run on same computer as client
SERVER_PORT = 5678

# HELPER SOCKET METHODS

def build_and_send_message(conn, code, data):
	"""
	Builds a new message using chatlib, wanted code and message. 
	Prints debug info, then sends it to the given socket.
	Paramaters: conn (socket object), code (str), data (str)
	Returns: Nothing
	"""
	# Implement Code
	

def recv_message_and_parse(conn):
	"""
	Recieves a new message from given socket,
	then parses the message using chatlib.
	Paramaters: conn (socket object)
	Returns: cmd (str) and data (str) of the received message. 
	If error occured, will return None, None
	"""
	# Implement Code
	# ..
	
	cmd, data = chatlib.parse_message(full_msg)
	return cmd, data
	
	

def connect():
    # Implement Code
    pass
    return socket


def error_and_exit(error_msg):
    # Implement code
    pass


def login(conn):
    username = input("Please enter username: \n")
    # Implement code
	
	build_and_send_message(conn, chatlib.PROTOCOL_CLIENT["login_msg"],"")
	
	# Implement code
	
    pass

def logout(conn):
    # Implement code
    pass

def main():
    # Implement code
    pass

if __name__ == '__main__':
    main()
