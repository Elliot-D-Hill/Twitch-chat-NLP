#!/usr/bin/python

import psycopg2
from config import config


def create_tables():
    """ create tables in the PostgreSQL database"""
    commands = (
        """
        CREATE TABLE IF NOT EXISTS chatlogs (
            comment_id SERIAL PRIMARY KEY,
            username VARCHAR(255) NOT NULL,
            channel VARCHAR(255) NOT NULL,
            datetime TIMESTAMP NOT NULL,
            comment VARCHAR(500) NOT NULL
        )
        """,
        """ CREATE TABLE IF NOT EXISTS inputs (
                text_id SERIAL PRIMARY KEY,
                username VARCHAR(255) NOT NULL
                )
        """)

    conn = None
    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # create table one by one
        for command in commands:
            cur.execute(command)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


if __name__ == '__main__':
    create_tables()
