import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """Create connection to SQLite database"""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    return conn

def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

sql_create_users_table = """CREATE TABLE IF NOT EXISTS users (
                            id integer PRIMARY KEY,
                            name text NOT NULL"""
conn = create_connection('database.db')
if conn is not None:
    create_table(conn,sql_create_users_table)