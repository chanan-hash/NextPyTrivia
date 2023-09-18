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


def login(conn: socket.socket):
    username = input("Please enter username: \n")
    password = input("Please enter password: \n")

    player = chatlib.join_data([username,password])


    build_and_send_message(conn, chatlib.PROTOCOL_CLIENT["login_msg"],"")
    cmd, data = recv_message_and_parse(conn)

#    while cmd != error_and_exit():


def logout(conn : socket.socket):
    """
    This functuion sending logout message by using 'build_and_send_message'
    :param conn:
    :return:
    """
    # chatlib.PROTOCOL_CLIENT["logout_msg"] --> A dictionary, for this is the key word for LOGOUT
    build_and_send_message(conn, chatlib.PROTOCOL_CLIENT["logout_msg"],"")

def main():
    """
    Main method.
    connect to server, login, logout, and close connection.
    """
    conn = connect() # Creating the socket
    login(conn)

    logout(conn)
    conn.close()
    print("Thanks for playing!!!")

if __name__ == '__main__':
    main()
