#!/usr/bin/python3

from config import config
from io import StringIO
import psycopg2
import pandas as pd


class Database:
    def __init__(self, filename, section):
        # read database configuration
        self._params = config(filename, section)
        # connect to the PostgreSQL database
        self.conn = psycopg2.connect(**self._params)
        # create a new cursor
        self._cursor = self.conn.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    @property
    def connection(self):
        return self.conn

    @property
    def cursor(self):
        return self._cursor

    def commit(self):
        self.connection.commit()

    def close(self, commit=True):
        if commit:
            self.commit()
        self.connection.close()

    def execute(self, sql, params=None):
        self.cursor.execute(sql, params or ())

    def fetchall(self):
        return self.cursor.fetchall()

    def fetchone(self):
        return self.cursor.fetchone()

    def query(self, sql, params=None):
        self.cursor.execute(sql, params or ())
        return self.fetchall()

    def executeSQLFromFile(self, filename):
        # Open and read the file as a single buffer
        fd = open(filename, 'r')
        sqlFile = fd.read()
        fd.close()
        # all SQL commands (split on ';')
        sqlCommands = sqlFile.strip(';').replace('\n', '').split(";")
        # Execute every command from the input file
        for command in sqlCommands:
            try:
                self.execute(command)
            except (Exception, psycopg2.DatabaseError) as error:
                print("Command skipped: ", command)

    def create_tables(self, filename):
        # create tables in the PostgreSQL database
        try:
            # create tables
            self.executeSQLFromFile(filename)
            # commit the changes
            self.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def insert_rows(self, dataframe, tablename, columns):
        # input dataframe to text stream
        buffer = StringIO()
        dataframe.to_csv(buffer, index=False, header=False)
        buffer.seek(0)
        try:
            # copy csv file to the table
            self.cursor.copy_from(
                file=buffer,
                table=tablename,
                columns=columns,
                sep=",")
            # commit the changes to the database
            self.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error: %s" % error)
            self.conn.rollback()
            self.close()
            return 1

    def create_df_from_table(self, sql_query, table):
        # query comments from the comments table
        try:
            # execute the SELECT statement
            self.execute(sql_query)
            # get all rows from table
            rows = self.fetchall()
            # get corresponding column names
            column_names = [desc[0] for desc in self.cursor.description]
            # convert table to dataframe
            df = pd.DataFrame(rows, columns=column_names)
            return df
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
