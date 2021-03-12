
import socket
import re
import pandas as pd
from datetime import datetime
from emoji import demojize


def log_chat(db, server, port, nickname, token, channel, max_batch_size):
    # connect socket to Twitch
    sock = socket.socket()
    sock.connect((server, port))
    sock.send(f"PASS {token}\n".encode('utf-8'))
    sock.send(f"NICK {nickname}\n".encode('utf-8'))
    sock.send(f"JOIN {channel}\n".encode('utf-8'))

    # a temporary list of comments data
    dict_list = []
    while True:
        # get response from Twitch socket
        response = sock.recv(2048).decode('utf-8')
        if response.startswith('PING'):
            sock.send("PONG\n".encode('utf-8'))
        elif len(response) > 0:
            # datetime object containing current date and time
            now = datetime.now()
            # format data: dd/mm/YY H:M:S
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            response = demojize(response)
            # capture username, channel, and user comment
            regex = ':(.*)\\!.*@.*\\.tmi\\.twitch\\.tv PRIVMSG #(.*) :(.*)'
            # enforce pattern matching for regular expression
            if re.search(regex, response) is not None:
                sentiment = None  # FIXME
                labeler = None  # FIXME
                username, channel, comment = re.search(
                    regex, response).groups()
                comment = comment.rstrip('\r')

                comment_dict = {
                    "username": username,
                    "channel": channel,
                    "date_time": dt_string,
                    "comment": comment,
                    "sentiment": sentiment,
                    "labeler": labeler}

                dict_list.append(comment_dict)

                if len(dict_list) >= max_batch_size:
                    comment_batch = pd.DataFrame.from_dict(dict_list)
                    db.insert_rows(
                        dataframe=comment_batch,
                        tablename="chat_logs",
                        columns=tuple(comment_dict.keys()))
                    dict_list = []

                # FIXME debug print
                print(
                    username,
                    channel,
                    dt_string,
                    comment,
                    sentiment,
                    labeler)
