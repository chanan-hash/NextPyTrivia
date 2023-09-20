import socket
import chatlib  # To use chatlib functions or consts, use chatlib.****

SERVER_IP = "127.0.0.1"  # Our server will run on same computer as client
SERVER_PORT = 5678

# HELPER SOCKET METHODS

def build_and_send_message(conn : socket.socket, code: str, data: str):
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


def build_send_recv_parse(conn: socket.socket, cmd: str, data: str) -> None:
    """
    This function suppose to shorten the proces by building the message and sending it
    Builds a new message using chatlib, wanted code and message.
    Then sends it to the given socket.
    After this, receives a new message from given socket,
    then parses the message using chatlib.
    Parameters: conn (socket object), code (str), data (str)
    Returns: cmd (str) and data (str) of the received message.
    If error occurred, will return None, None
    :rtype: object
    """
    build_and_send_message(conn,cmd,data)
    return recv_message_and_parse(conn) # this return 2 arguments, cnd and data

def connect():
    """
     Connect to the given server, return the open socket.
    :return: socket_server, a socket object
    """
    socket_server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    socket_server.connect((SERVER_IP,SERVER_PORT))
    print("connected to server...")

    return socket_server


def error_and_exit(error_msg: str):
    """
    Prints given error message, closes the program with error code 1
    :param error_msg: error message to print
    """
    print(error_msg)
    exit()


def login(conn: socket.socket) -> None:
    """
    Tries to log in user to server.
    get user and password from user and send to server.

    :param conn: socket object to communicate with server
    :return: None
    """
    while True:
        username = input("Please enter username: \n")
        password = input("Please enter password: \n")

        player = chatlib.join_data([username,password])

        build_and_send_message(conn, chatlib.PROTOCOL_CLIENT["login_msg"],player)
        cmd, data = recv_message_and_parse(conn)

        if cmd == chatlib.PROTOCOL_SERVER["login_ok_msg"]:
            print("Login successful!")
            return  # Exit the loop if login succeeds
        else:
            print("Login failed. Please try again.")


def logout(conn : socket.socket):
    """
    This functuion sending logout message by using 'build_and_send_message'
    :param conn:
    :return:
    """
    # chatlib.PROTOCOL_CLIENT["logout_msg"] --> A dictionary, for this is the key word for LOGOUT
    build_and_send_message(conn, chatlib.PROTOCOL_CLIENT["logout_msg"],"")

# Score functions
def get_score(conn: socket.socket) -> None:
    """
    This function printing the current score of the player
    :param conn:
    :return:player score
    """
    cmd, data = build_send_recv_parse(conn, chatlib.PROTOCOL_CLIENT["get_score_msg"],"")
    if cmd == chatlib.PROTOCOL_SERVER["get_score_msg"]: # means we got it correct
        print(f"your score is: {data}")
    else:
        error_and_exit("Error getting your score!")

def get_highscore(conn: socket.socket)-> None:
    """
    Gets highest score from server.
    :param conn:
    :return None:
    """
    cmd, data = build_send_recv_parse(conn, chatlib.PROTOCOL_CLIENT["get_high_score_msg"],"")
    if cmd == chatlib.PROTOCOL_SERVER["get_high_score_msg"]:
        print(f"High score is:\n{data}")
    else:
        error_and_exit("Error getting high score")

# Players functions
def play_question(conn: socket.socket):
    """
    Gets new question from the server,and print it to the user.
    Then get the user answer.

    If the server send NO_QUESTIONS, the game is end.
    If error occurred, the program will close.
    :param conn:
    :return:
    """
    cmd, data = build_send_recv_parse(conn, chatlib.PROTOCOL_CLIENT["get_question"], "")
    print(f"The question is: {data}")

    if cmd == chatlib.PROTOCOL_SERVER["no_questions"]:
        print("No more questions to you, the game is ended")
        return

    # check if the server send the question
    elif cmd == chatlib.PROTOCOL_SERVER["get_question"]:
        # split the data to question and answers
        split_data = chatlib.split_data(data, 6)

        if split_data is None:
            error_and_exit("Error play question - number of field is not 6")
            
        # id#question#answer1#answer2#answer3#answer4 --> the struct of a trivia question
        # After we've split it we can show it to the user
        question_id = split_data[0]
        question = split_data[1]
        print(f"Question: {question}\n\t1. {split_data[2]}\n\t2. {split_data[3]}\n\t3. {split_data[4]}\n\t3. {split_data[5]}")
        # This was showing the question

        # Getting the answer
        user_ans(conn,question_id)

    else:
        error_and_exit("Error play question - get wrong response")


# Help function to get the user ans, by question id
def user_ans(conn :socket.socket, question_id: str):
    """
    Gets answer from user, and send it to server.
    Then, print the response from the server.
    :param conn:
    :param question_id:
    :return:
    """
    ans = input("\n What is your answer (put a number 1-4): ")
    if not ans.isdigit() or int(ans) < 1 or int(ans) > 4: # checking if the user input is a valid number
        print("Invalid number for answer")

    # Sending he answer
    cmd, data = build_send_recv_parse(conn, chatlib.PROTOCOL_CLIENT["send_answer"],chatlib.join_data([question_id,ans]))

    # Chevking if this is the correct answer
    if cmd == chatlib.PROTOCOL_SERVER["correct_answer"]:
        print("Coreect answer, ver good!")
    elif cmd == chatlib.PROTOCOL_SERVER["wrong_answer"]:
        print(f"Wrong answer! the correct answer is: {data}")
    else:
        error_and_exit("Error play question")

def get_logged_users(conn: socket.socket):
    """
    Gets logged users from server.
   :param conn:
   :return:
    """
    cmd, data = build_send_recv_parse(conn, chatlib.PROTOCOL_CLIENT["get_login_players"], "")
    if cmd == chatlib.PROTOCOL_SERVER["get_login_players_msg"]:
        print(f"Logged users: \n{data}")
    else:
        error_and_exit("Error getting high score")


def main():
    """
    Main method.
    connect to server, login, logout, and close connection.
    """
    # Implement your main client functionality here
    # You can send and receive messages, interact with the server, etc.
    # Use build_and_send_message and recv_message_and_parse functions as needed.
    conn = connect() # Creating the socket
    login(conn)
    user_input = ""
    while user_input != "q":
        user_input = input("What is your choise:\n"
                           "p\t Play a trivia question\n"
                           "s\t Get my score\n"
                           "h\t Get the high score\n"
                           "l\t Get logged users\n"
                           "q\t Quit\n")
        if user_input == "p":
            play_question(conn)
        elif user_input == "s":
            get_score(conn)
        elif user_input == "h":
            get_highscore(conn)
        elif user_input == "l":
            get_logged_users(conn)
        elif user_input != "q":
            print("Thanks for playing!!!")
            break
    logout(conn)
    conn.close()
#    exit()


if __name__ == '__main__':
    main()
