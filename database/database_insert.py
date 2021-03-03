#!/usr/bin/python

import psycopg2
from config import config


def comment(username, channel, datetime, comment):
    # insert a new user comment into the chatlogs table
    sql = """INSERT INTO chatlogs(username, channel, datetime, comment)
             VALUES(%s, %s, %s, %s);"""
    conn = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        values = (username, channel, datetime, comment)
        cur.execute(sql, values)
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
