"""Contains methods for interacting with the backend database
Methods
-------
database_connection(func)
    Decorator that safely constructs and destructs the database
"""
import psycopg2

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
        except psycopg2.DatabaseError as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
                print("DB Closed")
            return output
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
    user_level,
    user_wallet,
    user_last_breed,
    user_warnings_issued,
    conn=None,):
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
