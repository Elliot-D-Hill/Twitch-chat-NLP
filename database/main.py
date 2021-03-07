#!/usr/bin/python

import query_table
import log_chat
import create_tables
import query_table

server = 'irc.chat.twitch.tv'
port = 6667
nickname = 'maieutikos'
token = 'oauth:dhvv3cupwmqz96goat55gpaxgcaxba'
channel = '#maieutikos'

# create PostgreSQL database tables, if they don't already exist
create_tables.create_tables()

sql_table = "chat_logs"
sql_query = f"SELECT * FROM {sql_table}"

corpus = query_table.get_data(sql_query, sql_table)

print(corpus)

# log user chats from specified channel to database
log_chat.log_chat(server, port, nickname, token, channel, max_batch_size=3)
