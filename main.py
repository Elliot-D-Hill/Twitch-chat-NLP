#!/usr/bin/python3

import config
import db.database
import app.chatbot

username = 'maieutikos'
token = config.OAUTH_TOKEN
channels = ['maieutikos']
# comment batch size before database insertion
max_batch_size = 1  # hint: larger batch sizes are more efficient

# initialize PostgreSQL database
twitch_db = db.database.Database(
    filename='db/database.ini', section='postgresql')

# initialize chat bot
bot = app.chatbot.ChatBot(twitch_db, username, token, channels)

# create tables in database, if they don't already exist
twitch_db.create_tables(filename='db/twitch_chat_tables.sql')

# connect to twitch chat and log user messages
bot.connect(max_batch_size)
