import os
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
                            userId integer PRIMARY KEY,
                            level integer NOT NULL,
                            wallet integer NOT NULL,
                            lastBreed string,
                            warnings_issued integer NOT NULL,
                            inventory string)
                        """
sql_create_creatures_table = """CREATE TABLE IF NOT EXISTS creatures (
                                creatureId integer PRIMARY KEY AUTOINCREMENT,
                                name text NOT NULL,
                                createDate integer NOT NULL,
                                imageLink text NOT NULL,
                                generation integer NOT NULL,
                                owner integer NOT NULL,
                                FOREIGN KEY (owner)
                                    REFERENCES users (userId)
                            )"""
sql_create_items_table = """CREATE TABLE IF NOT EXISTS items (
                            itemID integer PRIMARY KEY AUTOINCREMENT,
                            name text NOT NULL,
                            description text NOT NULL,
                            value integer NOT NULL,
                            imageLink string
                        )"""
db_file_prod=os.path.abspath(os.path.join(os.path.dirname(__file__), './database.db'))
conn = create_connection(db_file_prod)
if conn is not None:
    create_table(conn,sql_create_users_table)
    create_table(conn,sql_create_creatures_table)
    create_table(conn,sql_create_items_table)
    conn.close()
    conn = None

db_file_test=os.path.abspath(os.path.join(os.path.dirname(__file__), 'tests/database.db'))
conn = create_connection(db_file_test)
if conn is not None:
    create_table(conn,sql_create_users_table)
    create_table(conn,sql_create_creatures_table)
    create_table(conn,sql_create_items_table)
    sql =  f'''INSERT INTO users(userId,level,wallet,lastBreed,warnings_issued)
            VALUES(?,?,?,?,?)'''
    c = conn.cursor()
    c.execute(sql,(99999,99,0,"",0))
    conn.commit()
    conn.close()
