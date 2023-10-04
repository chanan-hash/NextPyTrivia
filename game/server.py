##############################################################################
# server.py
##############################################################################

import socket
import chatlib
import select

# GLOBALS
users = {}
questions = {}
logged_users = {} # a dictionary of client hostnames to usernames - will be used later
messages_to_send = [] # Sending messages for multiple clients
client_sockets_list = [] # For multiple clients

ERROR_MSG = "Error! "
SERVER_PORT = 5678
SERVER_IP = "127.0.0.1"


# HELPER SOCKET METHODS

def build_and_send_message(conn: socket, code: str, msg: str):
    ## copy from client
    """
    Builds a new message using chatlib, wanted code and message.
    Prints debug info, then sends it to the given socket.
    Paramaters: conn (socket object), code (str), data (str)
    Returns: Nothing
    """

    full_msg = chatlib.build_message(code, msg)
    print("[SERVER] ", conn.getpeername(), full_msg)  # Debug print
#    conn.send(full_msg.encode())
    messages_to_send.append((conn.getpeername(), full_msg))


def recv_message_and_parse(conn: socket.socket):
    ## copy from client
    """
    Recieves a new message from given socket,
    then parses the message using chatlib.
    Paramaters: conn (socket object)
    Returns: cmd (str) and data (str) of the received message.
    If error occured, will return None, None
    """
    full_msg = conn.recv(1024).decode()
    cmd, data = chatlib.parse_message(full_msg)

    print("[CLIENT] ", conn.getpeername(), full_msg)  # Debug print

    # Checking that the message we've got is ok
    if full_msg == "":
        return None, None

    if cmd is None:
        send_error(conn,"Error parsing message")

    if cmd == chatlib.PROTOCOL_SERVER["error_msg"]:
        send_error(conn, f"Error on receive your data. the data that received : {data}")

    return cmd, data



# Data Loaders #

def load_questions():
    """
    Loads questions bank from file	## FILE SUPPORT TO BE ADDED LATER
    Recieves: -
    Returns: questions dictionary
    """
    global questions
    questions = {
                2313 : {"question":"How much is 2+2","answers":["3","4","2","1"],"correct":2},
                4122 : {"question":"What is the capital of France?","answers":["Lion","Marseille","Paris","Montpellier"],"correct":3}
                }

    return questions

def load_user_database():
    """
    Loads users list from file	## FILE SUPPORT TO BE ADDED LATER
    Recieves: -
    Returns: user dictionary
    """
    global users
    users = {
            "test"		:	{"password":"test","score":0,"questions_asked":[]},
            "yossi"		:	{"password":"123","score":50,"questions_asked":[]},
            "master"	:	{"password":"master","score":200,"questions_asked":[]}
            }
    return users


# SOCKET CREATOR

def setup_socket():
    """
    Creates new listening socket and returns it
    Recieves: -
    Returns: the socket object
    """
    # Implement code ...
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.bind((SERVER_IP,SERVER_PORT))
    sock.listen()
    print("[SERVER] server up and running...")
    return sock




def send_error(conn: socket, error_msg: str) -> None:
    """
    Send error message with given message
    Recieves: socket, message error string from called function
    Returns: None
    """
    # Implement code ...
    build_and_send_message(conn, chatlib.PROTOCOL_SERVER["error_msg"], error_msg)


##### MESSAGE HANDLING


def handle_getscore_message(conn: socket.socket, username: str) -> None:
    global users
    # Implement this in later chapters

    score = users[username]["score"]
    build_and_send_message(conn, chatlib.PROTOCOL_SERVER["get_score_msg"], str(score))

def handle_highscore_message(conn: socket.socket) -> None:
    global users
    high_score = sorted(users, key=lambda u: users[u]["score"], reverse=True) # Getting the high score by sorting the data of the users

    the_high_score = ""
    for user in high_score: # Organizing the high score
        the_high_score = the_high_score + "\t" + user + ":" + str(users[user]["score"] + "\n")

    build_and_send_message(conn, chatlib.PROTOCOL_SERVER["get_high_score_msg"],the_high_score)

def handle_logged_message (conn : socket.socket):
    """
    Gets the logged in players and send them to the client.
    :param conn:
    :return:
    """
    global logged_users
    are_logged = ", ".join(logged_users.values())
    build_and_send_message(conn, chatlib.PROTOCOL_SERVER["get_login_players_msg"], are_logged)


def handle_logout_message(conn: socket.socket) -> None:
    """
    Closes the given socket (in later chapters, also remove user from logged_users dictioary)
    Receives: socket
    Returns: None
    """
    global logged_users
    # Implement code ...
#    username = logged_users.get(conn.getpeername())
    username = conn.getpeername()
    if username in logged_users:
        print(f"[SERVER]: User {username} ({conn.getpeername()}) disconnected")
        del logged_users[conn.getpeername()]
    client_sockets_list.remove(conn)
    conn.close()

#    print("[SERVER]: Disconnecting client, waiting for new connection")
 #   conn.close()


def handle_login_message(conn: socket.socket, data: str) -> None:
    """
    Gets socket and message data of login message. Checks  user and pass exists and match.
    If not - sends error and finished. If all ok, sends OK message and adds user and address to logged_users
    Recieves: socket, message code and data
    Returns: None (sends answer to client)
    """
    global users  # This is needed to access the same users dictionary from all functions
    global logged_users	 # To be used later

    # Implement code ...
    username_password = chatlib.split_data(data,2) # Splitting the data to username and password
    if username_password is None:
        send_error(conn, "Error on parsing your credentials")
        return

    # Checking the user nae and password if they are in the login list
    username = username_password[0]
    password = username_password[1]

    # One way strait forward
#	if username in users:
#		if password == users[username].password:
#			build_and_send_message(conn,chatlib.PROTOCOL_SERVER["login_ok_msg"], "")

#	else:
#		build_and_send_message(conn, chatlib.PROTOCOL_SERVER["login_failed_msg"], "Wrong credentials")
#		return

    # Second way, to do all in one condition. Instead of checking if the input (username & password are right) check if they're not on the list,
    # and if we've passed this condition they're right

    if username not in users or users[username]["password"] != password: # One of the is wrong, the order is first username and then checking  password
        build_and_send_message(conn, chatlib.PROTOCOL_SERVER["login_failed_msg"], "Wrong username or password")
        return

    # Checking if the user id all ready logged
    if username in logged_users.values():
        build_and_send_message(conn, chatlib.PROTOCOL_SERVER["login_failed_msg"], "User already logged in")
        return

    # Now if we passed those to conditions means the login is ok and we can send the client "LOGIN_OK" message
    logged_users[conn.getpeername()] = username  # Add user to logged users dict
    build_and_send_message(conn,chatlib.PROTOCOL_SERVER["login_ok_msg"], "")

    #if username in users:
     #   if users[username]["password"] == password:
    #        if not is_login(conn):
   #             build_and_send_message(conn, chatlib.PROTOCOL_SERVER["login_ok_msg"], "")
  #              logged_users[conn.getpeername()] = username
 #           else:
#                send_error(conn, "this user already login")
 #       else:
#            send_error(conn, "the password didn't match")
#    else:
#        send_error(conn, "the username doesn't exist")


def handle_client_message(conn: socket.socket, cmd, data):
    """
    Gets message code and data and calls the right function to handle command
    Recieves: socket, message code and data
    Returns: None
    """
    global logged_users	 # To be used later

    # Implement code ...

    # checking correction of command
    if cmd is None:
        send_error(conn, "Error on parsing your message")
        return

    if cmd == chatlib.PROTOCOL_CLIENT["login_msg"]:
        if conn.getpeername() in logged_users: # If the user is already logged
            send_error(conn, "You are already logged in!")
            return
    else:  	# If the command is not login, we check if the user is logged in
        if conn.getpeername() not in logged_users:
            send_error(conn, "You are not logged in!")
            return

    # If we've got here means the user may be inside
    if cmd == chatlib.PROTOCOL_CLIENT["login_msg"]:
        handle_login_message(conn,data)

    elif cmd == chatlib.PROTOCOL_CLIENT["logout_msg"]:
        handle_logout_message(conn)

    elif cmd == chatlib.PROTOCOL_CLIENT["get_score_msg"]:
        handle_getscore_message(conn, logged_users[conn.getpeername()])

    elif cmd == chatlib.PROTOCOL_CLIENT["get_high_score_msg"]:
        handle_highscore_message(conn)

    elif cmd == chatlib.PROTOCOL_CLIENT["get_login_players"]:
        handle_logged_message(conn)

def main():
    # Initializes global users and questions dicionaries using load functions, will be used later
    global users
    global questions
    global messages_to_send
    global client_sockets_list

    users = load_user_database()
    questions = load_questions()

    print("Welcome to Trivia Server!")
    # Implement code ...
    server_socket = setup_socket()

    while True:
        ready_to_read, ready_to_write, in_error = select.select([server_socket] + client_sockets_list, client_sockets_list, [])

        for current_socket in ready_to_read:
            if current_socket is server_socket: # New client joined in
                (client_socket, client_address) = current_socket.accept()
                print("New client connected!")
                client_sockets_list.append(client_socket)
            else:
                try: # Trying reading the message
                    cmd, data = recv_message_and_parse(current_socket)

                except ConnectionResetError:
                    print(f"[SERVER]: Client {current_socket.getpeername()} disconnected")
                    handle_logout_message(current_socket)
                    continue

            # If the client sent a logout message or an empty one to logout
                    if data is None or cmd == chatlib.PROTOCOL_CLIENT["logout_msg"]:
                        print(f"[SERVER]: Connection {current_socket.getpeername()} logged out!")
                        handle_logout_message(current_socket)

                    else:  # if the client send a valid message, we need to handle it
                        print(f"[SERVER]: client  {client_socket.getpeername()}, send: {data}")
                        handle_client_message(client_socket, cmd, data)

        # Answering all the sockets messages
        for socket_to_write in ready_to_write:
            for to_send in messages_to_send:
                if to_send[0] == socket_to_write.getpeername():
                    socket_to_write.send(to_send[1].encode())
                    messages_to_send.remove(to_send)


if __name__ == '__main__':
    main()

