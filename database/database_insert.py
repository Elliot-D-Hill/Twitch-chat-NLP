#!/usr/bin/python

import psycopg2
from io import StringIO
from config import config


def multiple_rows(df, table, columns):
    # Save the dataframe to disk as a csv file
    buffer = StringIO()
    df.to_csv(buffer, index=False, header=False)
    buffer.seek(0)
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # copy csv file to the table
        cur.copy_from(
            file=buffer,
            table=table,
            columns=columns,
            sep=",")
        # commit the changes to the database
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        conn.rollback()
        cur.close()
        return 1
    print(f"Finished inserting comments into {table} table")
    cur.close()
