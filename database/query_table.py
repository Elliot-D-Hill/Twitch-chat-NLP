#!/usr/bin/python

import psycopg2
import pandas as pd
from config import config


def get_data(sql_query, table):
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
        # get corresponding column names
        cur.execute(f"Select * FROM {table} LIMIT 0")
        column_names = [desc[0] for desc in cur.description]
        # close communication with the database
        cur.close()
        # convert table to dataframe
        df = pd.DataFrame(rows, columns=column_names)
        return df
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


if __name__ == '__main__':
    get_comments()
