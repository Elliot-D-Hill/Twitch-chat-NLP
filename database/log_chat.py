#!/usr/bin/python

import socket
import re
import pandas as pd
import database_insert
from datetime import datetime
from emoji import demojize


def log_chat(server, port, nickname, token, channel, max_batch_size):

    # a temporary list of comments data
    dict_list = []

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
            # capture username, channel, datetime, and user comment
            regex = ':(.*)\\!.*@.*\\.tmi\\.twitch\\.tv PRIVMSG #(.*) :(.*)'

            # enforce pattern matching for regular expression
            if re.search(regex, response) is not None:

                sentiment = None  # FIXME

                username, channel, comment = re.search(
                    regex, response).groups()
                comment = comment.rstrip('\r')

                comment_dict = {
                    "username": username,
                    "channel": channel,
                    "datetime": dt_string,
                    "comment": comment,
                    "sentiment": sentiment}

                dict_list.append(comment_dict)

                if len(dict_list) >= max_batch_size:
                    comment_batch = pd.DataFrame.from_dict(dict_list)
                    database_insert.multiple_rows(
                        df=comment_batch,
                        table="chat_logs",
                        columns=tuple(comment_dict.keys()))
                    dict_list = []

                print(
                    username,
                    channel,
                    dt_string,
                    comment,
                    sentiment)  # FIXME

# sock.close() ??? #FIXME
