"""Contains methods for interacting with the backend database
Methods
-------
database_connection(func)
    Decorator that safely constructs and destructs the database
"""
import psycopg2

def database_connection(func):
    def inner(*args,**kwargs):
        try:
            conn = psycopg2.connect(
                host="localhost",
                database="chorumfur",
                user="postgres",
                password="postgres"
            )
            output = func(conn,*args,**kwargs)
        except psycopg2.DatabaseError as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
                print("DB Closed")
        return output
    return inner
