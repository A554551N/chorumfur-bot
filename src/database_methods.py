"""Contains methods for interacting with the backend database
Methods
-------
database_connection(func)
    Decorator that safely constructs and destructs the database
"""

import psycopg2
import logging
import os
import pickle
from User import User
from Item import Item
from Creature import Creature
from Ticket import Ticket

f = open(os.path.abspath(os.path.join(os.path.dirname(__file__),'../db_pass.txt')),encoding='utf-8')
DB_PASSWORD = f.readline().rstrip('\n')

def make_database_connection(func):
    """Connects database connection and runs code passed from decorator"""
    def inner(*args,**kwargs):
        try:
            conn = psycopg2.connect(
                host="localhost",
                database="chorumfur",
                user="postgres",
                password=DB_PASSWORD
            )
            output = func(conn = conn,*args,**kwargs)
            if output:
                return output
            return False
        except psycopg2.DatabaseError as error:
            logging.warning(error)
        finally:
            if conn is not None:
                conn.close()
                logging.debug("DB Transaction Completed")
    return inner

@make_database_connection
def is_database_connected(conn=None):
    """Returns True if the database is connected"""
    if conn:
        return True
    return None

@make_database_connection
def add_user_to_database(user_to_add,conn=None):
    """Takes in a User object and adds to users table of db"""
    sql = """INSERT INTO users (
        user_id,
        user_level,
        user_wallet,
        user_lastBreed,
        user_warnings_issued)
        VALUES (%s,%s,%s,%s,%s)"""
    cur = conn.cursor()
    cur.execute(sql,(user_to_add.userId,
                     user_to_add.level,
                     user_to_add.wallet,
                     user_to_add.lastBreed,
                     user_to_add.warningsIssued))
    conn.commit()
    return True

@make_database_connection
def get_user_from_db(user_id,conn=None):
    """Retrieves a user from the database with a given ID and returns a User object."""
    sql = """SELECT user_level,user_wallet,user_lastBreed,user_warnings_issued
                FROM users WHERE user_id = %s
            """
    cur = conn.cursor()
    cur.execute(sql,(user_id,))
    user_data = cur.fetchone()
    if user_data:
        return User(userId = user_id,
                    level=user_data[0],
                    wallet=user_data[1],
                    lastBreed=user_data[2],
                    warningsIssued=user_data[3],
                    inventory=get_user_inventory(user_id))
    return None

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
        updated_quantity = retreived_row[1] + new_quantity
        owned_item_id = retreived_row[0]
        cur.execute(update_existing_item_row,(updated_quantity,owned_item_id))
        conn.commit()
    else:
        cur.execute(insert_new_item_row,(item_id,new_quantity,user_id))
        conn.commit()
    return True

@make_database_connection
def remove_item_from_user(user_id,item_id,quantity_to_remove=1,conn=None):
    """Removes a quantity of an item from a user-associated record in the owned_items db"""
    get_current_quantity = '''SELECT owned_item_id,owned_item_quantity FROM owned_items
                                WHERE owned_item_type_id=%s AND owned_item_owner=%s'''
    update_quantity = '''UPDATE owned_items
                         SET owned_item_quantity = %s
                         WHERE owned_item_id=%s'''
    delete_row = '''DELETE FROM owned_items
                    WHERE owned_item_id = %s'''
    cur = conn.cursor()
    cur.execute(get_current_quantity,(item_id,user_id))
    retreived_row = cur.fetchone()
    if retreived_row:
        row_id = retreived_row[0]
        current_quantity = retreived_row[1]
        if current_quantity <= quantity_to_remove:
            cur.execute(delete_row,(row_id,))
            conn.commit()
            return True
        quantity_remaining = current_quantity - quantity_to_remove
        cur.execute(update_quantity,(quantity_remaining,row_id))
        conn.commit()
        return True
    return False

@make_database_connection
def get_item_from_db(item_id,conn=None):
    """Retreives a record from the items database and returns an Item object"""
    get_item = '''SELECT item_id,item_name,item_desc,item_value,item_image_link
                FROM items WHERE item_id=%s'''
    cur = conn.cursor()
    cur.execute(get_item,(item_id,))
    retreived_row = cur.fetchone()
    if retreived_row:
        return Item(id=retreived_row[0],
                    name=retreived_row[1],
                    description=retreived_row[2],
                    value=retreived_row[3],
                    imageLink=retreived_row[4])
    return False

@make_database_connection
def add_item_to_db(item_to_add,conn=None):
    """Takes in an Item object and adds it to the items table of the database"""
    add_item_sql = '''INSERT INTO items (item_name,item_desc,item_value,item_image_link)
                  VALUES (%s,%s,%s,%s)
                  RETURNING item_id'''
    cur = conn.cursor()
    cur.execute(add_item_sql,(item_to_add.name,
                              item_to_add.description,
                              item_to_add.value,
                              item_to_add.imageLink))
    returned_id = cur.fetchone()[0]
    conn.commit()
    return returned_id

@make_database_connection
def get_all_items_from_db(conn=None):
    """Returns a list of all item types defined in the items table."""
    get_all_items_sql = """SELECT item_id,item_name,item_desc,item_value FROM items"""
    cur = conn.cursor()
    cur.execute(get_all_items_sql)
    returned_items = cur.fetchall()
    return returned_items


@make_database_connection
def get_user_inventory(user_id,conn=None):
    """Retreives all items associated with user and returns an array of tuples
    (Item object,quantity)"""
    get_inventory = '''SELECT items.item_id,
	                   items.item_name,
                       items.item_desc,
                       items.item_value,
                       items.item_image_link,
                       owned_items.owned_item_quantity
                       FROM items
                       INNER JOIN owned_items ON items.item_id = owned_items.owned_item_type_id
                       WHERE owned_items.owned_item_owner = %s'''
    cur = conn.cursor()
    cur.execute(get_inventory,(user_id,))
    retreived_rows = cur.fetchall()
    inventory = {}
    if retreived_rows:
        for row in retreived_rows:
            item_object = Item(id=row[0],
                        name=row[1],
                        description=row[2],
                        value=row[3],
                        imageLink=row[4])
            inventory[item_object.id] = (item_object,row[5])
        return inventory
    return None

@make_database_connection
def add_creature_to_db(creature_to_add,conn=None):
    """Takes in a Creature object and adds to creatures table of db.  Returns ID of added creture."""
    add_creature_sql = """INSERT INTO creatures
                          (creature_name,
                          creature_owner,
                          creature_create_date,
                          creature_image_link,
                          creature_generation,
                          creature_traits,
                          creature_parent_a,
                          creature_parent_b)
                          VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
                          RETURNING creature_id
                          """
    cur = conn.cursor()
    cur.execute(add_creature_sql,
                (creature_to_add.name,
                 creature_to_add.owner,
                 creature_to_add.createDate,
                 creature_to_add.imageLink,
                 creature_to_add.generation,
                 pickle.dumps(creature_to_add.traits),
                 creature_to_add.parents[0],
                 creature_to_add.parents[1]))
    returned_id = cur.fetchone()[0]
    conn.commit()
    return returned_id

@make_database_connection
def get_creature_from_db(creature_id,conn=None):
    """Takes in an int creature_id and returns a matching Creature object from db"""
    get_creature_sql = """SELECT creature_name,
                                 creature_owner,
                                 creature_id,
                                 creature_create_date,
                                 creature_image_link,
                                 creature_generation,
                                 creature_traits,
                                 creature_parent_a,
                                 creature_parent_b
                          FROM creatures
                          WHERE creature_id = %s"""
    cur = conn.cursor()
    cur.execute(get_creature_sql,(creature_id,))
    returned_row = cur.fetchone()
    if returned_row:
        returned_creature = Creature(name=returned_row[0],
                                     owner=returned_row[1],
                                     creatureId=returned_row[2],
                                     createDate=returned_row[3],
                                     imageLink=returned_row[4],
                                     generation=returned_row[5])
        if returned_row[6]:
            returned_creature.traits=pickle.loads(returned_row[6])
        if returned_row[7] or returned_row[8]:
            returned_creature.parents = [returned_row[7],returned_row[8]]
        return returned_creature
    return None

@make_database_connection
def get_parents_from_db(creature,conn=None):
    """Takes in a Creature object and returns an array of Creature objects for parents"""
    get_parents_sql = """SELECT creature_name,
                                 creature_owner,
                                 creature_id,
                                 creature_create_date,
                                 creature_image_link,
                                 creature_generation,
                                 creature_traits,
                                 creature_parent_a,
                                 creature_parent_b
                          FROM creatures
                          WHERE creature_id = %s OR creature_id = %s"""
    cur = conn.cursor()
    cur.execute(get_parents_sql,(creature.parents[0],creature.parents[1]))
    returned_rows = cur.fetchall()
    if returned_rows:
        returned_parents = []
        for returned_row in returned_rows:
            returned_creature = Creature(name=returned_row[0],
                                         owner=returned_row[1],
                                         creatureId=returned_row[2],
                                         createDate=returned_row[3],
                                         imageLink=returned_row[4],
                                         generation=returned_row[5])
            if returned_row[6]:
                returned_creature.traits=pickle.loads(returned_row[6])
            if returned_row[7] or returned_row[8]:
                returned_creature.parents = [returned_row[7],returned_row[8]]
            returned_parents.append(returned_creature)
        return returned_parents
    return None

@make_database_connection
def update_user_last_breed(user,conn=None):
    update_user_sql = """UPDATE users
                         SET user_lastbreed = %s
                         WHERE user_id = %s"""
    cur = conn.cursor()
    cur.execute(update_user_sql,(user.lastBreed,user.userId))
    conn.commit()
    return True

@make_database_connection
def add_ticket_to_db(ticket,conn=None):
    """Adds a ticket object to the database, returns added ID"""
    add_ticket_sql = """INSERT INTO breeding_tickets
                        (ticket_name,
                        ticket_requestor,
                        ticket_date,
                        ticket_status,
                        ticket_creature_a,
                        ticket_creature_b)
                        VALUES (%s,%s,%s,%s,%s,%s)
                        RETURNING ticket_id"""
    cur = conn.cursor()
    cur.execute(add_ticket_sql,(ticket.name,
                                ticket.requestor.userId,
                                ticket.ticket_date,
                                ticket.status,
                                ticket.creature_a.creatureId,
                                ticket.creature_b.creatureId))
    returned_id = cur.fetchone()[0]
    conn.commit()
    return returned_id
    
if __name__ == "__main__":
    creature_a = get_creature_from_db(27)
    creature_b = get_creature_from_db(28)
    user = get_user_from_db(202632427535859712)
    test_ticket = Ticket("Test Ticket",user,creature_a,creature_b)
    add_ticket_to_db(test_ticket)
