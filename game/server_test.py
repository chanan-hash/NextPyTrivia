##############################################################################
# server.py
##############################################################################

# Contributed by:
# https://github.com/sasonii/networks-campus.il/blob/main/server.py#L195


import socket
import chatlib
import select
import random
import copy
import json
import requests
import base64

path = r'C:\Users\Lam\Documents\Code\Python\Networks\משימה מתגלגלת\u1'
http_api_questions = "https://opentdb.com/api.php?amount=50&type=multiple"
# http_api_questions = "https://opentdb.com/api.php?amount=50&type=multiple&encode=base64"
# GLOBALS
users = {}
questions = {}
logged_users = {}  # a dictionary of client hostnames to usernames - will be used later
messages_to_send = []

MAX_MSG_LENGTH = 1024
ERROR_MSG = "Error! "
SERVER_PORT = 5678
SERVER_IP = "127.0.0.1"


# HELPER SOCKET METHODS

def build_and_send_message(conn, code, data):
    global messages_to_send
    full_msg = chatlib.build_message(code, data)
    messages_to_send.append((conn, full_msg))
    # Debug print


def recv_message_and_parse(conn):
    full_msg = conn.recv(MAX_MSG_LENGTH).decode()
    cmd, data = chatlib.parse_message(full_msg)

    print("[CLIENT] ", full_msg)  # Debug print
    return cmd, data


def build_send_recv_parse(conn, code, data):
    build_and_send_message(conn, code, data)
    msg_code, data = recv_message_and_parse(conn)
    return msg_code, data


# Data Loaders #

def load_questions():
    """
    Loads questions bank from file	## FILE SUPPORT TO BE ADDED LATER
    Recieves: -
    Returns: questions dictionary
    """
    with open(path + r'\questions.json', 'r') as questions_json:
        questions = json.load(questions_json)
    # questions = {
    #             2313 : {"question":"How much is 2+2","answers":["3","4","2","1"],"correct":2},
    #             4122 : {"question":"What is the capital of France?","answers":["Lion","Marseille","Paris","Montpellier"],"correct":3}
    #             }

    return questions


def load_questions_from_web():
    """
    Loads questions bank from file	## FILE SUPPORT TO BE ADDED LATER
    Recieves: -
    Returns: questions dictionary
    """

    r = requests.get(http_api_questions)
    json_content = json.loads(r.content)
    # with open(r"C:\Users\Lam\Documents\Code\Python\Networks\questions_web.json", 'r') as j:
    #     json_content = json.load(j)
    del json_content['response_code']
    questions = {}
    for index_question, question in enumerate(json_content['results']):
        correct_answer = question["correct_answer"]
        all_answers = [correct_answer] + question["incorrect_answers"]
        random.shuffle(all_answers)
        correct_answer_index = all_answers.index(correct_answer)
        fixed_replaced_question = question["question"].replace("&#039;", "'").replace("&quot;", "'")
        if (fixed_replaced_question.find('#') != -1 or fixed_replaced_question.find('|') != -1):
            break
        print(fixed_replaced_question)
        questions[str(index_question)] = {
            "question": fixed_replaced_question,
            "answers": all_answers,
            "correct": str(correct_answer_index + 1)
        }
    print(len(questions))
    return questions


def load_user_database():
    """
    Loads users list from file	## FILE SUPPORT TO BE ADDED LATER
    Recieves: -
    Returns: user dictionary
    """
    with open(path + r'\users.json', 'r') as users_json:
        users = json.load(users_json)
    # users = {
    #         "test"		:	{"password":"test","score":0,"questions_asked":[]},
    #         "yossi"		:	{"password":"123","score":50,"questions_asked":[]},
    #         "master"	:	{"password":"master","score":200,"questions_asked":[]}
    #         }
    return users


def edit_user_value(username, argument, *value):
    global users
    if argument == "score":
        users[username]["score"] += 5
    elif argument == "questions_asked":
        users[username]["questions_asked"].append(value[0])
    with open(path + r'\users.json', 'w') as users_json:
        json.dump(users, users_json)


def create_random_question(username):
    global users
    questions_id = list(questions.keys())
    questions_id_asked = users[username]["questions_asked"]
    questions_id_removed_asked = [question_id for question_id in questions_id if
                                  str(question_id) not in questions_id_asked]
    if questions_id_removed_asked == []:
        return None
    random_key = questions_id_removed_asked[random.randint(0, len(questions_id_removed_asked) - 1)]
    question = questions[random_key]["question"]
    answers = questions[random_key]["answers"]
    formatted_question = chatlib.join_data([random_key] + [question] + answers)
    edit_user_value(username, "questions_asked", random_key)
    print("\n", formatted_question, random_key)
    return formatted_question


# SOCKET CREATOR

def setup_socket():
    """
    Creates new listening socket and returns it
    Recieves: -
    Returns: the socket object
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_IP, SERVER_PORT))
    server_socket.listen()

    return server_socket


def send_error(conn, error_msg):
    """
    Send error message with given message
    Recieves: socket, message error string from called function
    Returns: None
    """
    build_and_send_message(conn, chatlib.PROTOCOL_SERVER["login_failed_msg"], ERROR_MSG + error_msg)


##### MESSAGE HANDLING


def handle_getscore_message(conn, username):
    global users
    user_score = users[username]["score"]
    build_and_send_message(conn, chatlib.PROTOCOL_SERVER["your_score_msg"], str(user_score))


def handle_logged_message(conn):
    global logged_users
    msg_to_send = ','.join([logged_users[user] for user in logged_users])
    build_and_send_message(conn, chatlib.PROTOCOL_SERVER["logged_answer_msg"], msg_to_send)


def handle_question_message(conn):
    msg_to_send = create_random_question(logged_users[conn.getpeername()])
    if msg_to_send is None:
        build_and_send_message(conn, chatlib.PROTOCOL_SERVER["no_questions_msg"], "")
        return
    build_and_send_message(conn, chatlib.PROTOCOL_SERVER["your_question_msg"], msg_to_send)


def handle_answer_message(conn, username, data):
    global users
    global questions
    data_parts = data.split(chatlib.DATA_DELIMITER)
    question_id_in_data = 0
    if question_id_in_data in users[username]["questions_asked"]:
        send_error(conn, "Forbidden, you have already answered this question.")
    answer_id_in_data = 1
    question_id = int(data_parts[question_id_in_data])
    answer = int(data_parts[answer_id_in_data])
    correct_answer = questions[str(question_id)]["correct"]
    if (int(correct_answer) == answer):
        build_and_send_message(conn, chatlib.PROTOCOL_SERVER["correct_answer_msg"], "")
        edit_user_value(username, "score")
        return
    build_and_send_message(conn, chatlib.PROTOCOL_SERVER["wrong_answer_msg"], str(correct_answer))


def sorted_scores(all_users):
    users = copy.copy(all_users)
    sorted_scores_users = {}
    while users != {}:
        maximum_score = users[list(users)[0]]["score"]
        maximum_score_user = list(users)[0]
        for user in users:
            if users[user]["score"] > maximum_score:
                maximum_score = users[user]["score"]
                maximum_score_user = user
        sorted_scores_users[maximum_score_user] = maximum_score
        del users[maximum_score_user]
    return sorted_scores_users


def handle_highscore_message(conn):
    global users
    scores = sorted_scores(users)
    msg_to_send = "".join([user + ":" + str(scores[user]) + "\n" for user in scores])
    build_and_send_message(conn, chatlib.PROTOCOL_SERVER["all_score_msg"], msg_to_send)


def handle_logout_message(conn):
    """
    Closes the given socket (in laster chapters, also remove user from logged_users dictioary)
    Recieves: socket
    Returns: None
    """
    global logged_users
    del logged_users[conn.getpeername()]
    conn.close()


def handle_login_message(conn, data):
    """
    Gets socket and message data of login message. Checks user and pass exists and match.
    If not - sends error and finished. If all ok, sends OK message and adds user and address to logged_users
    Recieves: socket, message code and data
    Returns: None (sends answer to client)
    """
    global users  # This is needed to access the same users dictionary from all functions
    global logged_users  # To be used later
    username = data.split(chatlib.DATA_DELIMITER)[0]
    password = data.split(chatlib.DATA_DELIMITER)[1]
    if username in users.keys():
        if users[username]["password"] == password:
            build_and_send_message(conn, chatlib.PROTOCOL_SERVER["login_ok_msg"], "")
            logged_users[conn.getpeername()] = username
            return
    send_error(conn, "Wrong username or password!")


def handle_client_message(conn, cmd, data):
    """
    Gets message code and data and calls the right function to handle command
    Recieves: socket, message code and data
    Returns: None
    """

    global logged_users

    if not cmd in chatlib.PROTOCOL_CLIENT.values():
        send_error(conn, "No such command")
    else:
        if not conn.getpeername() in logged_users.keys():
            if cmd == "LOGIN":
                handle_login_message(conn, data)
        else:
            if cmd == "LOGOUT":
                handle_logout_message(conn)
            elif cmd == "MY_SCORE":
                handle_getscore_message(conn, logged_users[conn.getpeername()])
            elif cmd == "HIGHSCORE":
                handle_highscore_message(conn)
            elif cmd == "LOGGED":
                handle_logged_message(conn)
            elif cmd == "GET_QUESTION":
                handle_question_message(conn)
            elif cmd == "SEND_ANSWER":
                handle_answer_message(conn, logged_users[conn.getpeername()], data)


def print_client_sockets(client_sockets):
    for c in client_sockets:
        print("\t", c.getpeername())


def main():
    # Initializes global users and questions dicionaries using load functions, will be used later
    global users
    global questions
    global messages_to_send

    users = load_user_database()

    questions = load_questions_from_web()
    print("Welcome to Trivia Server!")

    print("Setting up server...")
    server_socket = setup_socket()
    print("Listening for clients...")
    client_sockets = []
    while True:
        ready_to_read, ready_to_write, in_error = select.select([server_socket] + client_sockets, client_sockets, [])
        for current_socket in ready_to_read:
            if current_socket is server_socket:
                (client_socket, client_address) = current_socket.accept()
                print("New client joined!, Waiting to chcek his details.", client_address)
                client_sockets.append(client_socket)
                print_client_sockets(client_sockets)
            else:
                try:
                    cmd, data = recv_message_and_parse(current_socket)
                    handle_client_message(current_socket, cmd, data)
                    if (cmd == "LOGOUT"):
                        client_sockets.remove(current_socket)

                except (ConnectionAbortedError, ConnectionResetError) as e:
                    print(str(e))
                    print("\t", current_socket.getpeername(), "cloesed the connection")
                    client_sockets.remove(current_socket)
                    handle_logout_message(current_socket)
                    print_client_sockets(client_sockets)

        for message in messages_to_send:
            current_socket, data = message
            if current_socket in ready_to_write:
                current_socket.send(data.encode())
                messages_to_send.remove(message)
                print("[SERVER] ", data)
        # print("Waiting for new connection...")


if __name__ == '__main__':
    main()
