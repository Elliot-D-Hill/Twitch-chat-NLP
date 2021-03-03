#!/usr/bin/python

import socket
import re
import database_insert
from datetime import datetime
from emoji import demojize


def log_chat(server, port, nickname, token, channel):

    sock = socket.socket()

    # connect socket to Twitch
    sock.connect((server, port))

    sock.send(f"PASS {token}\n".encode('utf-8'))
    sock.send(f"NICK {nickname}\n".encode('utf-8'))
    sock.send(f"JOIN {channel}\n".encode('utf-8'))

    while True:
        response = sock.recv(2048).decode('utf-8')

        if response.startswith('PING'):
            sock.send("PONG\n".encode('utf-8'))

        elif len(response) > 0:
            # datetime object containing current date and time
            now = datetime.now()
            # format data: dd/mm/YY H:M:S
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

            response = demojize(response)
            regex = ':(.*)\\!.*@.*\\.tmi\\.twitch\\.tv PRIVMSG #(.*) :(.*)'

            # enforce pattern matching for regular expression
            if re.search(regex, response) is not None:
                username, channel, comment = re.search(
                    regex, response).groups()
                comment = comment.rstrip('\r')
                database_insert.comment(username, channel, dt_string, comment)
                print(username, channel, dt_string, comment)  # FIXME

# sock.close()
