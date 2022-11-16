"""Performs initial database setup in accordance with defined schema"""
import psycopg2

SQL_CREATE_USERS_TABLE = """
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY,
    user_level INTEGER NOT NULL,
    user_wallet INTEGER NOT NULL,
    user_lastBreed TEXT NOT NULL,
    user_warnings_issed INTEGER NOT NULL
    )"""

SQL_CREATE_CREATURES_TABLE = """
CREATE TABLE creatures (
    creature_id SERIAL PRIMARY KEY,
    creature_name TEXT NOT NULL,
    creature_create_date TEXT NOT NULL,
    creature_image_link TEXT NOT NULL,
    creature_generation INTEGER NOT NULL,
    creature_owner INTEGER NOT NULL,
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
    owned_item_owner INTEGER NOT NULL,
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
def setup_database():
    """Performs initial database setup for application"""
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="chorumfur",
            user="postgres",
            password="postgres"
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

if __name__ == '__main__':
    setup_database()
