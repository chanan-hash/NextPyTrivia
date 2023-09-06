# from chatlib_skeleton import *
from typing import List, Tuple, Union

DATA_DELIMITER = "#"  # Delimiter in the data part of the message


def split_data(msg, expected_fields):
    count = 0
    for str in msg:
        if (str == "#"):
            count += 1
    if count != expected_fields:
        return [None]
    else:
        fields = msg.split("#")
        return fields


print(split_data("username#password", 1))
print(split_data("user#name#pass#word", 2))
print(split_data("username", 2))
print(split_data("user#name#pass#word", 3))
print()


def join_data(msg_fields):
    for str in msg_fields:
        joined_msg = "#".join(msg_fields)
    return joined_msg


str = ['username', 'password']
print(join_data(str))
print(join_data(["question", "ans1", "ans2", "ans3", "ans4", "correct"]))

cmd = "execute"
CMD_FIELD_LENGTH = 15
cmd_part = cmd.ljust(CMD_FIELD_LENGTH)
print(cmd_part)
