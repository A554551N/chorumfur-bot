import os
import Creature
import User
from Item import Item
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
        conn.close()
        return None
    creatureId = c.lastrowid
    conn.close()
    return creatureId

def getCreatureFromDB(creatureId,test=False):
    """Collects a creature record from the DB by Creature ID and returns a Creature Object

        Parameters
        ----------
        creatureId : int
            the desired CreatureId
        test : bool
            flag True to direct to Test DB
        
        Returns
        -------
        Creature
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
    if result:
        return Creature.Creature(name=result[0][1],
                            owner=result[0][5],
                            imageLink=result[0][3],
                            generation=result[0][4],
                            creatureId=result[0][0],
                            createDate=result[0][2]
                            )
    return None

def getUserInventory(user,test=False):
    """Collects all items on the ownedItems table that belong to a given User
    and returns an updated User object
    
    PARAMETERS
    ----------
    user : User Object
        User object to update
    test : bool
        flag True to use test environment
    
    Returns a User"""

    sql='''SELECT items.itemId,
            name,
            description,
            value,
            imageLink
        FROM
            items
        INNER JOIN
    ownedItems ON items.itemID = ownedItems.itemID
    WHERE ownedItems.owner = ?'''
    conn = create_connection(test)
    c = conn.cursor()
    c.execute(sql,(user.userId,))
    results = c.fetchall()
    conn.close()
    if results:
        inventory = {}
        for result in results:
            if result[0] in inventory.keys():
                inventory[result[0]][1] = inventory[result[0]][1] + 1
            else:
                inventory[result[0]] = [Item(result[1],result[2],result[3],result[4],result[0]),1]
        user.inventory = inventory
    return user

def addItemToDB(itemToAdd,test=False):
    """
    Adds a new Item to the user database

    Paramters
    ---------
    itemToAdd : Item object
        an item object to add to the DB
    test : bool
        flag True to use Test Route
    """
    itemAttributes = (f"{itemToAdd.name}",
                        f"{itemToAdd.description}",
                        f"{itemToAdd.value}",
                        f"{itemToAdd.imageLink}"
                    )

    sql =  f'''INSERT INTO items(name,description,value,imageLink)
            VALUES(?,?,?,?)'''
    conn = create_connection(test)
    c = conn.cursor()
    try:
        c.execute(sql,itemAttributes)
        conn.commit()
    except Error as e:
        conn.close()
        return None
    itemId = c.lastrowid
    conn.close()
    print("Successful Add")
    return itemId

def getAllItemsInDB(test=False):
    sql = '''SELECT
                itemId,
                name,
                description,
                value
                FROM items
            '''
    conn = create_connection(test)
    c = conn.cursor()
    c.execute(sql)
    result = c.fetchall()
    output = "**ID/Name/Description/Value**\n"
    count=0
    for i in range(len(result)):
        for x in range(len(result[i])):
            output+= f"{result[i][x]}/"
        output+="\n"
        count+=1
    output+= f"**Total Records Returned:** {count}"
    return output