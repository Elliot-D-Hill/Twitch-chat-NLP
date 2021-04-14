
from db import database
from twitch_nlp import chatbot
import config


def main():
    username = 'deviousdata'
    token = config.OAUTH_TOKEN
    channels = ['deviousdata']
    # comment batch size before database insertion
    max_batch_size = 1  # hint: larger batch sizes are more efficient

    # initialize PostgreSQL database
    twitch_database = database.Database(
        filename='db/database.ini', section='postgresql')

    # initialize chat bot
    bot = chatbot.ChatBot(twitch_database, username, token, channels)

    # create tables in database, if they don't already exist
    twitch_database.create_tables(filename='db/twitch_chat_tables.sql')

    # connect to twitch chat and log user messages
    bot.connect(max_batch_size)


if __name__ == "__main__":
    main()
