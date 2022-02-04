import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def create_table(conn):
    """create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """

    sql_create_giveaways_table = """ CREATE TABLE IF NOT EXISTS giveaways (
                                        id integer PRIMARY KEY,
                                        server_id text NOT NULL,
                                        channel_id text NOT NULL,
                                        message_id text NOT NULL
                                    ); """
    try:
        c = conn.cursor()
        c.execute(sql_create_giveaways_table)
    except Error as e:
        print(e)


def add_message_id(conn, server_id, channel_id, message_id):
    sql_insert_statement = """ INSERT INTO giveaways (server_id,channel_id,message_id) VALUES ({},{},{}); """.format(
        server_id, channel_id, message_id
    )
    try:
        c = conn.cursor()
        c.execute(sql_insert_statement)
        conn.commit()
        return True
    except Error as e:
        print(e)
        return False


def check_message_id(conn, server_id, channel_id, message_id):
    sql_insert_statement = """ select * from giveaways where server_id = {} and channel_id = {} and message_id = {}; """.format(
        server_id, channel_id, message_id
    )
    try:
        c = conn.cursor()
        c.execute(sql_insert_statement)
        rows = c.fetchall()
        if len(rows) > 0:
            return True
        else:
            return False
    except Error as e:
        print(e)
        return None
