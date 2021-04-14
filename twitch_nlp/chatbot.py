#!/usr/bin/env python

import socket
import re
from pandas import DataFrame
from emoji import demojize
from datetime import datetime


class ChatBot:
    def __init__(self, database, username, token, channels):
        self.database = database
        self.username = username
        self.token = token
        self.channels = channels
        self.server = 'irc.chat.twitch.tv'
        self.port = 6667
        self.irc_socket = None

    def send_command(self, command):
        if 'PASS' not in command:
            print(f'< {command}')
        self.irc_socket.send((command + '\r\n').encode('utf-8'))

    def send_privmsg(self, channel, text):
        self.send_command(f'PRIVMSG #{channel} :{text}')

    def connect(self, max_batch_size):
        # connect socket to Twitch
        self.irc_socket = socket.socket()
        self.irc_socket.connect((self.server, self.port))
        self.send_command(f'PASS {self.token}')
        self.send_command(f'NICK {self.username}')
        for channel in self.channels:
            self.send_command(f'JOIN #{channel}')
            self.send_privmsg(
                channel, 'TwitchBot online. Hacking into the mainframe...')
        self.log_messages(max_batch_size)

    def handle_response(self, response):
        msg = Message(response)
        # captures username, channel, and comment from message
        regex = ':(.*)\\!.*@.*\\.tmi\\.twitch\\.tv PRIVMSG #(.*) :(.*)'
        if re.search(regex, msg.text):
            msg.parse(regex)
            return msg
        else:
            return None

    def log_messages(self, max_batch_size):
        table_name = 'chat_logs'
        table_col_names = self.database.get_table_col_names(table_name)
        # a temporary list of message data
        comment_batch = []
        while True:
            # get response from Twitch socket
            response = self.irc_socket.recv(2048).decode()
            print(response)
            msg = self.handle_response(response)
            if response.startswith('PING'):
                self.irc_socket.send("PONG\n".encode('utf-8'))
            # true if valid comment
            elif len(response) > 0 and msg:
                # create row for database insertion
                message_dict = {key: msg.data[key]
                                for key in table_col_names[1:]}
                # add row to comment batch
                comment_batch.append(message_dict)
                # true if comment batch size is reached
                if len(comment_batch) >= max_batch_size:
                    message_batch = DataFrame.from_dict(comment_batch)
                    # add comment batch to database
                    self.database.insert_rows(
                        dataframe=message_batch,
                        tablename=table_name,
                        columns=tuple(message_dict.keys()))
                    comment_batch = []


class Message:
    def __init__(self, text):
        self.text = text
        self.data = {'date_time': None,
                     'username': None,
                     'channel': None,
                     'sentiment': None,
                     'labeler': None,
                     'receiver': None,
                     'comment': None,
                     'comment_command': None,
                     'comment_args': None}

    def parse_comment(self):
        # convert emojis to text and strip newline
        self.data['comment'] = demojize(self.data['comment']).rstrip('\r')
        self.data['sentiment'] = None  # FIXME
        self.data['labeler'] = None  # FIXME
        self.data['receiver'] = None  # FIXME

    def parse(self, regex):
        # enforce pattern matching for regular expression
        if re.search(regex, self.text):
            username, channel, comment = re.search(regex, self.text).groups()
            # get datatime as format: YY/mm/dd H:M:S
            self.data['date_time'] = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S")
            self.data['username'] = username
            self.data['channel'] = channel
            self.data['comment'] = comment
            self.parse_comment()
