from typing import List
# Protocol Constants

CMD_FIELD_LENGTH = 16  # Exact length of cmd field (in bytes)
LENGTH_FIELD_LENGTH = 4  # Exact length of length field (in bytes)
MAX_DATA_LENGTH = 10 ** LENGTH_FIELD_LENGTH - 1  # Max size of data field according to protocol
MSG_HEADER_LENGTH = CMD_FIELD_LENGTH + 1 + LENGTH_FIELD_LENGTH + 1  # Exact size of header (CMD+LENGTH fields)
MAX_MSG_LENGTH = MSG_HEADER_LENGTH + MAX_DATA_LENGTH  # Max size of total message
DELIMITER = "|"  # Delimiter character in protocol
DATA_DELIMITER = "#"  # Delimiter in the data part of the message

# Protocol Messages 
# In this dictionary we will have all the client and server command names

# A dictionary for client server commands
PROTOCOL_CLIENT = {
    "login_msg": "LOGIN",
    "logout_msg": "LOGOUT",
    "get_login_players": "LOGGED",
    "get_question": "GET_QUESTION",
    "send_answer": "SEND_ANSWER",
    "get_score_msg": "MY_SCORE",
    "get_high_score_msg": "HIGHSCORE",
}  # .. Add more commands if needed

PROTOCOL_SERVER = {
    "error_msg": "ERROR",
    "login_ok_msg": "LOGIN_OK",
    "login_failed_msg": "LOGIN_FAILED",
    "get_login_players_msg": "LOGGED_ANSWER",
    "get_question": "YOUR_QUESTION",
    "correct_answer": "CORRECT_ANSWER",
    "wrong_answer": "WRONG_ANSWER",
    "get_score_msg": "YOUR_SCORE",
    "get_high_score_msg": "ALL_SCORE",
    "no_questions": "NO_QUESTIONS",
}  # ..  Add more commands if needed

# Other constants

ERROR_RETURN = None  # What is returned in case of an error


def build_message(cmd: str, data: str):
    """
    Gets command name (str) and data field (str) and creates a valid protocol message
    Returns: str, or None if error occured
    """
    # if the command is not one of the known commands, return None
    if cmd not in PROTOCOL_SERVER.values() and cmd not in PROTOCOL_CLIENT.values():
        return None

    # if the command is more than the allowed length
    if len(cmd) > MSG_HEADER_LENGTH:
        return None
    if len(data) > MAX_DATA_LENGTH:
        return None
    # cmd_part = f'{cmd}{" " * (CMD_FIELD_LENGTH - len(cmd))}' --> it puts the cmd, and adding spaces as needed:
    # The total length(16) minus the length of the cmd, and all of it as a String format. f' allows us in the String format to get other functions or variables, like the cmd.
    cmd_part = cmd.ljust(CMD_FIELD_LENGTH)
    # zfill --> means zero fill, it wirte the length of the data, and padding it with zero.
    # emp': if data length is 10, so after filling/padding with zero (4 times as the constant "LENGTH_FIELD_LENGTH", see above)
    # 00010, and all of it in a String format
    data_len_part = str(len(data)).zfill(LENGTH_FIELD_LENGTH)
    full_msg = f'{cmd_part}|{data_len_part}|{data}'

    return full_msg


def parse_message(data: str):  # data : str, means that the function is getting a String, because in python ypu don't need to define the type like in java.
    # it helps us in the function when we reference to 'data', to operate String methods on it
    """
    Parses protocol message and returns command name and data field
    Returns: cmd (str), data (str). If some error occured, returns None, None
    """
    # First of all we are checking if the input is correct, if not, we'll return None, None

    # Checking if the data is incorrect, or if its to long
    if data is None or len(data) > MAX_MSG_LENGTH:
        return None, None

    # Splitting the input according to "|" to brake the message to parts
    dataSplit = data.split(DELIMITER)  # --> [LOGIN,0009,aaaa#bbbb] exmp'

    # The message needs to be built from 3 parts: "LOGIN | 0009 | aaaa#bbbb" exmp'
    if len(dataSplit) != 3:
        return None, None

    # Checking if the cmd (command) is in the right length
    if len(dataSplit[0]) != CMD_FIELD_LENGTH:
        return None, None

    # Now we are handling each part of the message in separate

    # checking the middle/password (the four numbers) if it in the right length (4), and if it is numbers and not something else
    if len(dataSplit[1]) != 4 or not dataSplit[1].isdigit():
        return None, None

    cmd = dataSplit[0].replace(" ", "")  # Taking to the spaces, so we return only the command itself, "Noise clean"

    # checking if the length of the password is correct according to what th message is, and if all data has been received
    MidData = int(dataSplit[1])
    msg = dataSplit[2]
    if len(msg) != MidData:
        return None, None

    # The function should return 2 values
    return cmd, msg


def split_data(msg: str, expected_fields: int):
    """
    Helper method. gets a string and number of expected fields in it. Splits the string
    using protocol's data field delimiter (|#) and validates that there are correct number of fields.
    Returns: list of fields if all ok. If some error occured, returns None
    """
    # count = 0
    # for str in msg:
    #	if (str == "#"):
    #		count += 1
    #	if count != expected_fields:
    #		return [None]
    #	else:
    #		fields = msg.split("#")
    #		return fields

    if msg is None or msg.count(DATA_DELIMITER) != expected_fields - 1:
        return None
    return msg.split(DATA_DELIMITER)


def join_data(msg_fields: List[str]):
    """
    Helper method. Gets a list, joins all of it's fields to one string divided by the data delimiter.
    Returns: string that looks like cell1#cell2#cell3
    """
    #	for str in msg_fields:
    #		joined_msg = "#".join(msg_fields)
    #	return joined_msg
    return DATA_DELIMITER.join(msg_fields)


