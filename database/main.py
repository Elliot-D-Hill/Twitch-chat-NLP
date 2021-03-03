#!/usr/bin/python

import log_chat
import create_table

server = 'irc.chat.twitch.tv'
port = 6667
nickname = 'maieutikos'
token = 'oauth:dhvv3cupwmqz96goat55gpaxgcaxba'
channel = '#maieutikos'

create_table.create_tables()
log_chat.log_chat(server, port, nickname, token, channel)
