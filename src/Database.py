import os
import Creature
import User
import pickle
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

def addUserToDB(userToAdd,test=False):
    """
    Adds a new user to the user database

    Paramters
    ---------
    userToAdd : User object
        a user object to add to the DB
    test : bool
        flag True to use Test Route
    """
    userAttributes = (f"{userToAdd.userId}",
                        f"{userToAdd.level}",
                        f"{userToAdd.wallet}",
                        f"{userToAdd.lastBreed}",
                        f"{userToAdd.warningsIssued}"
                    )

    sql =  f'''INSERT INTO users(userId,level,wallet,lastBreed,warnings_issued)
            VALUES(?,?,?,?,?)'''
    conn = create_connection(test)
    c = conn.cursor()
    try:
        c.execute(sql,userAttributes)
        conn.commit()
    except Error as e:
        conn.close()
        return None
    userId = c.lastrowid
    conn.close()
    return True

def getUserFromDB(userId,test=False):
    """
    Collects User record from Database and returns a User object

    Parameters
    ----------
    userId : int
        userId to search database for
    test : bool
        flag True to use test route
    """
    sql = '''SELECT
                userId,
                level,
                wallet,
                lastBreed,
                warnings_issued
            FROM users
            WHERE userId=?
            '''
    conn = create_connection(test)
    c = conn.cursor()
    c.execute(sql,(userId,))
    result = c.fetchall()
    conn.close()
    if result:
        return User.User(
            userId=result[0][0],
            level=result[0][1],
            wallet=result[0][2],
            lastBreed=result[0][3],
            warningsIssued=result[0][4])
    return None

# STORE/GET INVENTORY
def addToUserInventory(ownerId,itemId,test):
    '''Add an item to the ownedItem DB and associate it with a given owner
    Parameters
    ---------
    ownerId : int
        the owner Id to insert
    itemId : int
        the id of the item from the items DB
    test: bool
        flag true to route to test DB'''

    sql='''INSERT INTO ownedItems (itemID,quantity,owner)
            VALUES (?,?,?)'''
    conn = create_connection(test)
    c = conn.cursor()
    try:
        c.execute(sql,(itemId,1,ownerId))
        conn.commit()
    except Error as e:
        conn.close()
        return e
        #return None
    conn.close()
    return "Record has been successfully added"
    #return True

# Mothballing this method while code is refactored.
"""
def storeInventory(user,test=False):
    sql='''UPDATE users SET inventory = ? WHERE userId = ?;'''
    inventoryToStore = pickle.dumps(user.inventory)
    conn = create_connection(test)
    c = conn.cursor()
    try:
        c.execute(sql,(inventoryToStore,user.userId))
        conn.commit()
    except Error as e:
        conn.close()
        return None
    conn.close()
    return True
"""
def getInventory(user,test=False):
    sql='''SELECT inventory FROM users WHERE userId = ?'''
    conn = create_connection(test)
    c = conn.cursor()
    c.execute(sql,(user.userId,))
    result = c.fetchall()
    conn.close()
    if result:
        user.inventory = pickle.loads(result[0][0])
        return user
    return None

# Add/Get Item from DB

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

def getItemFromDB(itemID,test=False):
    '''
    Get an existing item from the database and return an Item object
    
    Parameters
    ----------
    itemID : int
        the requested itemID
    test : bool
        flag True to use Test Route
    '''

    sql = '''SELECT
                itemId,
                name,
                description,
                value,
                imageLink
                FROM items
                WHERE itemId = ?
            '''

    conn = create_connection(test)
    c = conn.cursor()
    c.execute(sql,(itemID,))
    result = c.fetchall()
    conn.close()
    if result:
        return Item(result[0][1],result[0][2],result[0][3],result[0][4],result[0][0])
    return None

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
    
#if conn is not None:
#    take DB actions here
#conn.close()

print(addToUserInventory(99999,800,True))