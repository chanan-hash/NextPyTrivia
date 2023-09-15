import socket
import chatlib  # To use chatlib functions or consts, use chatlib.****

SERVER_IP = "127.0.0.1"  # Our server will run on same computer as client
SERVER_PORT = 5678

# HELPER SOCKET METHODS

def build_and_send_message(conn : socket.socket, code, data):
    """
    Builds a new message using chatlib, wanted code and message.
    Prints debug info, then sends it to the given socket.
    Paramaters: conn (socket object), code (str), data (str)
    Returns: Nothing
    """

    info = chatlib.build_message(code,data)
    print(f"Client sent: {info}")
    conn.send(info.encode())

# conn: socket.socket --> means that the type on 'conn' is a socket object so we can operate on it socket functions
def recv_message_and_parse(conn: socket.socket):
    """
    Recieves a new message from given socket,
    then parses the message using chatlib.
    Paramaters: conn (socket object)
    Returns: cmd (str) and data (str) of the received message.
    If error occured, will return None, None
    """
    full_msg = conn.recv(1024).decode()
    cmd, data = chatlib.parse_message(full_msg)

    # Checking that the message we've got are ok
    if cmd is None:
        error_and_exit("Error parsing message")

    if cmd == chatlib.PROTOCOL_SERVER["error_msg"]:
        error_and_exit(f"Error: {data}")

    return cmd, data



def connect():
    """
     Connect to the given server, return the open socket.
    :return: socket_server, a socket object
    """
    socket_server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    socket_server.connect((SERVER_IP,SERVER_PORT))
    print("connected to server...")

    return socket_server


def error_and_exit(error_msg):
    """
    Prints given error message, closes the program with error code 1
    :param error_msg: error message to print
    """
    print(error_msg)
    exit()


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
