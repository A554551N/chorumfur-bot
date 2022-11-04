import os
import sqlite3
from sqlite3 import Error

def create_connection(test=False):
    """Create connection to SQLite database"""
    if test:
        db_file = (os.path.abspath(os.path.join(os.path.dirname(__file__), '../tests/database.db')))
    else:
        db_file=os.path.abspath(os.path.join(os.path.dirname(__file__), '../database.db'))
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

def addCreatureToDB(creatureToAdd,test=False):
    '''Adds a Creature record to the DB

    Parameters
    ----------
    creaturetoAdd : Creature object
        a Creature object to be added to the DB
    test : bool
        directs the request to the test environment
    '''
    creatureAttributes = (f"{creatureToAdd.name}",
                        f"{creatureToAdd.createDate}",
                        f"{creatureToAdd.imageLink}",
                        f"{creatureToAdd.generation}",
                        f"{creatureToAdd.owner}")
    sql = f'''INSERT INTO creatures(name,createDate,imageLink,generation,owner)
            VALUES(?,?,?,?,?)
        '''
    conn = create_connection(test)
    c = conn.cursor()
    try:
        c.execute(sql,creatureAttributes)
        conn.commit()
    except Error as e:
        print(e)
    creatureId = c.lastrowid
    conn.close()
    return creatureId

def getCreatureFromDB(creatureId,test=False):
    """Collects a creature record from the DB by Creature ID

        Parameters
        ----------
        creatureId : int
            the desired CreatureId
        test : bool
            flag True to direct to Test DB
    """
    sql = '''SELECT
                creatureId,
                name,
                createDate,
                imageLink,
                generation,
                owner
            FROM creatures
            WHERE creatureId=?
            '''
    conn = create_connection(test)
    c = conn.cursor()
    c.execute(sql,(creatureId,))
    result = c.fetchall()
    conn.close()
    return result


    

#if conn is not None:
#    take DB actions here
#conn.close()