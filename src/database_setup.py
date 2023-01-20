"""Performs initial database setup in accordance with defined schema"""
import os
import psycopg2

SQL_CREATE_USERS_TABLE = """
CREATE TABLE users (
    user_id BIGINT PRIMARY KEY,
    user_level INTEGER NOT NULL,
    user_wallet INTEGER NOT NULL,
    user_lastBreed TEXT,
    user_warnings_issued INTEGER NOT NULL
    )"""

SQL_CREATE_CREATURES_TABLE = """
CREATE TABLE creatures (
    creature_id SERIAL PRIMARY KEY,
    creature_name TEXT NOT NULL,
    creature_create_date TEXT NOT NULL,
    creature_image_link TEXT NOT NULL,
    creature_generation INTEGER NOT NULL,
    creature_owner BIGINT NOT NULL,
    creature_traits TEXT,
    CONSTRAINT fk_user
        FOREIGN KEY(creature_owner)
            REFERENCES users(user_id)
    )"""

SQL_CREATE_ITEMS_TABLE = """
CREATE TABLE items (
    item_id SERIAL PRIMARY KEY,
    item_name TEXT NOT NULL,
    item_desc TEXT NOT NULL,
    item_value INTEGER NOT NULL,
    item_image_link TEXT
    )"""

SQL_CREATE_OWNED_ITEMS_TABLE = """
CREATE TABLE owned_items(
    owned_item_id SERIAL PRIMARY KEY,
    owned_item_type_id INTEGER NOT NULL,
    owned_item_quantity INTEGER,
    owned_item_owner BIGINT NOT NULL,
    CONSTRAINT fk_user
        FOREIGN KEY(owned_item_owner)
            REFERENCES users(user_id),
    CONSTRAINT fk_item
    FOREIGN KEY(owned_item_type_id)
        REFERENCES items(item_id)
    )"""

SQL_COMMANDS = (
    SQL_CREATE_USERS_TABLE,
    SQL_CREATE_CREATURES_TABLE,
    SQL_CREATE_ITEMS_TABLE,
    SQL_CREATE_OWNED_ITEMS_TABLE
)

def setup_databases(database_name,database_password):
    """Performs initial database setup for application"""
    try:
        conn = psycopg2.connect(
            host="localhost",
            database=database_name,
            user="postgres",
            password=database_password
        )

        cur = conn.cursor()
        for command in SQL_COMMANDS:
            cur.execute(command)
        cur.close()
        conn.commit()
    except (psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print("DB Closed")

f = open(os.path.abspath(os.path.join(os.path.dirname(__file__),'../db_pass.txt')),encoding='utf-8')
database_password = f.readline().rstrip('\n')

if __name__ == '__main__':
    print(database_password)
    setup_databases('chorumfur',database_password)
