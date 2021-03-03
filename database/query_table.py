#!/usr/bin/python

import psycopg2
from config import config


def get_data(sql_query):
    """ query comments from the comments table """
    conn = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the SELECT statement
        cur.execute(sql_query)
        # get all rows from table
        rows = cur.fetchall()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return rows


if __name__ == '__main__':
    get_comments()
