import os
import socket

from config import settings


def remove_spaces(str):
    r = ""
    for i in range(len(str)):
        if not str[i].isspace():
            r += str[i]
    return r


def get_attributes(str):
    str = remove_spaces(str)
    attr_vals = {}
    markers = []
    for i in range(len(str)):
        if str[i] == "'" or str[i] == '"':          # if we come upon a quote
            if i == 0 or str[i-1] != '\\':          # ignore the quote if it is escaped
                markers.append(i)
    if len(markers)%2 != 0:                         # must have an even number of quotes to be valid
        raise RuntimeError("get_attributes received a string whose quotes don't match up.")
    for i in range(0, len(markers)-1, 2):
        val = str[markers[i]+1:markers[i+1]]        # get string between the markers
        if i == 0:
            attr = str[:markers[i]-1]               # -1 to get rid of the equals sign (we know there won't be spaces)
        else:
            attr = str[markers[i-1]+1:markers[i]-1] # -1 to get rid of quote and equals sign
        attr_vals.update({attr:val})
    return attr_vals


def find_last(target, str):
    for i in range(len(str)-1, -1, -1):
        if str[i] == target:
            return i
    return -1


def get_config(file_name):
    r = {}
    try:
        file = open(os.path.join(settings.BASE_DIR, "config/" + file_name), "r")
    except OSError:
        return None
    lines = file.readlines()
    for line in lines:
        comment_free_line = remove_comment(line, "#")
        key_vals = comment_free_line.split(":")
        if len(key_vals) > 1:
            r.update({key_vals[0].strip(): key_vals[1].strip()})
    file.close()
    return r


def remove_comment(line, comment_start):
    try:
        ind = line.index(comment_start)
        return line[:ind]
    except ValueError:
        return line


def get_ip():
    """
    A method to get the ip address of this machine. Connects to address
    8.8.8.8 (Google's public DNS) and then looks at the name of the
    socket. Returns this as a string.
    :return: A string representing the ip address of this machine.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.connect(("8.8.8.8", 80))
    ip = sock.getsockname()[0]
    sock.close()
    return ip
