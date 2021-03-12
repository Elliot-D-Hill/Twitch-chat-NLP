#!/usr/bin/python3

import log_chat
import database

server = 'irc.chat.twitch.tv'
port = 6667
nickname = 'maieutikos'
token = 'oauth:dhvv3cupwmqz96goat55gpaxgcaxba'
channel = '#maieutikos'
max_batch_size = 3  # comment batch size before insertion

db = database.Database(filename='database.ini', section='postgresql')

# create tables in database, if they don't already exist
db.create_tables(filename='twitch_chat_tables.sql')

sql_table = "chat_logs"
sql_query = f"SELECT * FROM {sql_table}"

corpus = db.create_df_from_table(sql_query, sql_table)

if not corpus.empty:
    print(corpus.tail())

# log user chats from specified channel to database
log_chat.log_chat(
    db=db,
    server=server,
    port=port,
    nickname=nickname,
    token=token,
    channel=channel,
    max_batch_size=max_batch_size)
