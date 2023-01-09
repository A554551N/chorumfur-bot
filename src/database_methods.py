"""Contains methods for interacting with the backend database
Methods
-------
database_connection(func)
    Decorator that safely constructs and destructs the database
"""
import psycopg2
from User import User

def make_database_connection(func):
    """Connects database connection and runs code passed from decorator"""
    def inner(*args,**kwargs):
        try:
            conn = psycopg2.connect(
                host="localhost",
                database="chorumfur",
                user="postgres",
                password="postgres"
            )
            output = func(conn = conn,*args,**kwargs)
            if output:
                return output
            return False
        except psycopg2.DatabaseError as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
                print("DB Closed")
    return inner

@make_database_connection
def is_database_connected(conn=None):
    """Returns True if the database is connected"""
    if conn:
        return True
    return None

@make_database_connection
def add_user_to_database(
    user_id,
    user_level=1,
    user_wallet=0,
    user_last_breed="",
    user_warnings_issued=0,
    conn=None):
    """Adds a user to the Users table of the database"""
    sql = """INSERT INTO users (
        user_id,
        user_level,
        user_wallet,
        user_lastBreed,
        user_warnings_issued)
        VALUES (%s,%s,%s,%s,%s)"""
    cur = conn.cursor()
    cur.execute(sql,(user_id,user_level,user_wallet,user_last_breed,user_warnings_issued))
    conn.commit()
    return True

@make_database_connection
def get_user_from_db(user_id,conn=None):
    """Retrieves a user from the database with a given ID"""
    sql = """SELECT user_level,user_wallet,user_lastBreed,user_warnings_issued
                FROM users WHERE user_id = %s
            """
    cur = conn.cursor()
    cur.execute(sql,(user_id,))
    user_data = cur.fetchall()
    return User(userId = user_id,
        level=user_data[0][0],
        wallet=user_data[0][1],
        lastBreed=user_data[0][2],
        warningsIssued=user_data[0][3])

@make_database_connection
def add_item_to_user(user_id,item_id,new_quantity=1,conn=None):
    """Adds an item to the owned_items database associated to user_id"""
    check_if_item_type_owned = '''SELECT owned_item_id,owned_item_quantity FROM owned_items
                                    WHERE owned_item_type_id = %s AND owned_item_owner = %s'''
    insert_new_item_row='''INSERT INTO owned_items (owned_item_type_id,owned_item_quantity,owned_item_owner)
            VALUES (%s,%s,%s)'''
    update_existing_item_row='''UPDATE owned_items
                                SET owned_item_quantity = %s
                                WHERE owned_item_id = %s'''
    cur = conn.cursor()
    cur.execute(check_if_item_type_owned,(item_id,user_id))
    retreived_row = cur.fetchone()
    if retreived_row:
        print(retreived_row)
        updated_quantity = retreived_row[1] + new_quantity
        owned_item_id = retreived_row[0]
        cur.execute(update_existing_item_row,(updated_quantity,owned_item_id))
        conn.commit()
    else:
        cur.execute(insert_new_item_row,(item_id,new_quantity,user_id))
        conn.commit()
    return True