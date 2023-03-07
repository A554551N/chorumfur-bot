"""Contains methods for interacting with the backend database
Methods
-------
make_database_connection(func)
    Decorator that safely constructs and destructs the database

is_database_connected()
    Returns True if database is connected

add_user_to_db()
    adds a user with given parameters to the database

get_user_from_db()
    queries the db for a given user ID and returns a User object

add_item_to_user()
    adds an item with a given ID to a given user's inventory

remove_item_from_user()
    removes an item with a given ID from a given user's inventory

get_item_from_db()
    queries the db for a given Item ID and returns an Item object

add_item_to_db()
    adds an item with given parameters to the items db

get_all_items_from_db()
    returns all items defined in the items db

get_user_inventory():
    queries the owned_items table for all Items associated with a user,
    returns a tuple of records

add_creature_to_db():
    adds a creature with given parameters to the db
"""

import psycopg2
import psycopg2.extras
import logging
import os
import pickle
from User import User
from Item import Item
from Creature import Creature
from Ticket import Ticket
from ConstantData import Constants

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
        user_warnings_issued,
        user_pending_breeding)
        VALUES (%s,%s,%s,%s,%s,%s)"""
    cur = conn.cursor()
    cur.execute(sql,(user_to_add.userId,
                     user_to_add.level,
                     user_to_add.wallet,
                     user_to_add.lastBreed,
                     user_to_add.warningsIssued,
                     user_to_add.is_breeding_pending))
    conn.commit()
    return True

@make_database_connection
def update_currency_in_wallet(user_id,amount_change,conn=None):
    """Adds or removes currency from a user record in the database
    
    Parameters
    -----------
    user_id: int
        user ID to change
    amount_change: int
        amount to add or remove (expressed as a positive or negative int)
    """

    wallet_sql = """UPDATE users
                    SET user_wallet = user_wallet+%s
                    WHERE user_id = %s"""
    cur = conn.cursor()
    cur.execute(wallet_sql,(amount_change,user_id))
    conn.commit()
    return True

@make_database_connection
def get_user_from_db(user_id,conn=None):
    """Retrieves a user from the database with a given ID and returns a User object."""
    sql = """SELECT user_id,user_level,user_wallet,user_lastBreed,user_warnings_issued,user_pending_breeding
                FROM users WHERE user_id = %s
            """
    cur = conn.cursor()
    cur.execute(sql,(user_id,))
    user_data = cur.fetchone()
    if user_data:
        return pack_user(user_data)
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
    """Returns a tuple of tuples conataining all item types defined in the items table."""
    get_all_items_sql = """SELECT item_id,item_name,item_value FROM items"""
    cur = conn.cursor()
    cur.execute(get_all_items_sql)
    returned_items = cur.fetchall()
    return returned_items


@make_database_connection
def get_user_inventory(user_id,conn=None):
    """Retreives all items associated with user and returns a tuple of tuples
    (Item ID, Item Name, Item Quantity)"""
    get_inventory = '''SELECT items.item_id,
	                   items.item_name,
                       owned_items.owned_item_quantity
                       FROM items
                       INNER JOIN owned_items ON items.item_id = owned_items.owned_item_type_id
                       WHERE owned_items.owned_item_owner = %s'''
    cur = conn.cursor()
    cur.execute(get_inventory,(user_id,))
    retreived_rows = cur.fetchall()
    if retreived_rows:
        return retreived_rows
    return None

@make_database_connection
def add_creature_to_db(creature_to_add,conn=None):
    """Takes in a Creature object and adds to creatures table of db.  Returns ID of added creture."""
    add_creature_sql = """INSERT INTO creatures
                          (creature_name,
                          creature_owner,
                          creature_create_date,
                          creature_image_link,
                          creature_image_link_newborn,
                          creature_image_link_pup,
                          creature_generation,
                          creature_traits,
                          creature_parent_a,
                          creature_parent_b,
                          creature_available_to_breed,
                          creature_is_active,
                          creature_last_forage)
                          VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                          RETURNING creature_id
                          """
    cur = conn.cursor()
    cur.execute(add_creature_sql,
                (creature_to_add.name,
                 creature_to_add.owner,
                 creature_to_add.createDate,
                 creature_to_add.imageLink,
                 creature_to_add.imageLink_nb,
                 creature_to_add.imageLink_pup,
                 creature_to_add.generation,
                 pickle.dumps(creature_to_add.traits),
                 creature_to_add.parents[0],
                 creature_to_add.parents[1],
                 creature_to_add.available_to_breed,
                 creature_to_add.is_active,
                 creature_to_add.last_forage))
    returned_id = cur.fetchone()[0]
    conn.commit()
    return returned_id

@make_database_connection
def add_multiple_creatures_to_db(creature_list,conn=None):
    """Takes in a list of Creature objects and adds them to the creatures table of db.
    Returns a tuple of IDs for the added creatures."""
    add_creature_sql = """INSERT INTO creatures
                          (creature_name,
                          creature_owner,
                          creature_create_date,
                          creature_image_link,
                          creature_image_link_newborn,
                          creature_image_link_pup,
                          creature_generation,
                          creature_traits,
                          creature_parent_a,
                          creature_parent_b,
                          creature_available_to_breed,
                          creature_is_active,
                          creature_last_forage)
                          VALUES %s
                          RETURNING creature_id
                          """
    list_to_add = []
    for creature_to_add in creature_list:
        list_to_add.append((creature_to_add.name,
                 creature_to_add.owner,
                 creature_to_add.createDate,
                 creature_to_add.imageLink,
                 creature_to_add.imageLink_nb,
                 creature_to_add.imageLink_pup,
                 creature_to_add.generation,
                 pickle.dumps(creature_to_add.traits),
                 creature_to_add.parents[0],
                 creature_to_add.parents[1],
                 creature_to_add.available_to_breed,
                 creature_to_add.is_active,
                 creature_to_add.last_forage))
    cur = conn.cursor()
    returned_ids = psycopg2.extras.execute_values(cur,add_creature_sql,list_to_add,fetch=True)
    conn.commit()
    return returned_ids

@make_database_connection
def get_creature_from_db(creature_id,conn=None):
    """Takes in an int creature_id and returns a matching Creature object from db"""
    get_creature_sql = """SELECT creature_name,
                                 creature_owner,
                                 creature_id,
                                 creature_create_date,
                                 creature_image_link,
                                 creature_image_link_newborn,
                                 creature_image_link_pup,
                                 creature_generation,
                                 creature_traits,
                                 creature_parent_a,
                                 creature_parent_b,
                                 creature_available_to_breed,
                                 creature_is_active,
                                 creature_last_forage
                          FROM creatures
                          WHERE creature_id = %s"""
    cur = conn.cursor()
    cur.execute(get_creature_sql,(creature_id,))
    returned_row = cur.fetchone()
    if returned_row:
        return pack_creature(returned_row)
    return None

@make_database_connection
def update_creature(creature_to_update,conn=None):
    update_creature_sql = '''
                          UPDATE creatures
                          SET creature_name = %s,
                              creature_image_link = %s,
                              creature_image_link_newborn = %s,
                              creature_image_link_pup = %s,
                              creature_owner = %s,
                              creature_traits = %s,
                              creature_create_date = %s,
                              creature_available_to_breed = %s
                          WHERE creature_id = %s
                          '''
    cur = conn.cursor()
    cur.execute(update_creature_sql,(creature_to_update.name,
                                     creature_to_update.imageLink,
                                     creature_to_update.imageLink_nb,
                                     creature_to_update.imageLink_pup,
                                     creature_to_update.owner,
                                     pickle.dumps(creature_to_update.traits),
                                     creature_to_update.createDate,
                                     creature_to_update.available_to_breed,
                                     creature_to_update.is_active,
                                     #creature_to_update.last_forage,
                                     #creature_to_update.creatureId
                                     ))
    if cur.rowcount == 1:
        conn.commit()
        return True
    return False
@make_database_connection
def get_parents_from_db(creature,conn=None):
    """Takes in a Creature object and returns an array of Creature objects for parents"""
    get_parents_sql = """SELECT creature_name,
                                 creature_owner,
                                 creature_id,
                                 creature_create_date,
                                 creature_image_link,
                                 creature_image_link_newborn,
                                 creature_image_link_pup,
                                 creature_generation,
                                 creature_traits,
                                 creature_parent_a,
                                 creature_parent_b,
                                 creature_available_to_breed,
                                 creature_is_active,
                                 creature_last_forage
                          FROM creatures
                          WHERE creature_id = %s OR creature_id = %s"""
    cur = conn.cursor()
    cur.execute(get_parents_sql,(creature.parents[0],creature.parents[1]))
    returned_rows = cur.fetchall()
    if returned_rows:
        returned_parents = []
        for returned_row in returned_rows:
            returned_creature = pack_creature(returned_row)
            returned_parents.append(returned_creature)
        return returned_parents
    return None

@make_database_connection
def get_my_creatures_from_db(user_id,conn=None):
    """Retreives all creatures from the database with a given user_id.
    Returns creature_id and creature_name"""
    get_creatures_sql="""SELECT creature_id,
                                creature_name
                        FROM creatures
                        WHERE creature_owner = %s
                        ORDER BY creature_id ASC"""
    cur = conn.cursor()
    cur.execute(get_creatures_sql,(user_id,))
    returned_rows = cur.fetchall()
    if returned_rows:
        return returned_rows
    return None

@make_database_connection
def get_creatures_available_to_breed(conn=None):
    """Retrieve all creatures marked available to breed and return them"""
    get_creatures_sql = """SELECT creature_id,
                                  creature_name
                           FROM creatures
                           WHERE creature_available_to_breed = True
                           ORDER BY creature_id ASC"""
    cur = conn.cursor()
    cur.execute(get_creatures_sql)
    returned_rows = cur.fetchall()
    return returned_rows or None

@make_database_connection
def get_wild_chorumfur_ids(conn=None):
    """Retrieves all creature records with an owner of 0"""
    get_creatures_sql = """SELECT creature_id
                           FROM creatures
                           WHERE creature_owner = 0"""
    cur = conn.cursor()
    cur.execute(get_creatures_sql)
    return cur.fetchall() or None

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
def update_user_pending_breeding(user,conn=None):
    update_user_sql = """UPDATE users
                         SET user_pending_breeding = %s
                         WHERE user_id = %s"""
    cur = conn.cursor()
    cur.execute(update_user_sql,(user.is_breeding_pending,user.userId))
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
                        ticket_creature_b,
                        ticket_pups)
                        VALUES (%s,%s,%s,%s,%s,%s,%s)
                        RETURNING ticket_id"""
    cur = conn.cursor()
    pickled_pups = pickle.dumps(ticket.pups)
    cur.execute(add_ticket_sql,(ticket.name,
                                ticket.requestor.userId,
                                ticket.ticket_date,
                                ticket.status,
                                ticket.creature_a.creatureId,
                                ticket.creature_b.creatureId,
                                pickled_pups))
    returned_id = cur.fetchone()[0]
    conn.commit()
    return returned_id

@make_database_connection
def get_ticket_from_db(ticket_id,conn=None):
    """Gets a ticket from the DB by ID and returns a Ticket object"""
    get_ticket_sql = """SELECT ticket_id,
                               ticket_name,
                               ticket_requestor,
                               ticket_date,
                               ticket_status,
                               ticket_creature_a,
                               ticket_creature_b,
                               ticket_pups
                        FROM breeding_tickets
                        WHERE ticket_id=%s"""
    cur = conn.cursor()
    cur.execute(get_ticket_sql,(ticket_id,))
    result = cur.fetchone()
    if result:
        requestor = get_user_from_db(result[2])
        tkt_creature_a = get_creature_from_db(result[5])
        tkt_creature_b = get_creature_from_db(result[6])
        tkt_pups = pickle.loads(result[7])
        returned_ticket =Ticket(
            ticket_name = result[1],
            ticket_requestor = requestor,
            creature_a = tkt_creature_a,
            creature_b = tkt_creature_b,
            ticket_id=result[0],
            ticket_date=result[3],
            ticket_status=result[4],
            pups = tkt_pups)
        return returned_ticket
    return None

@make_database_connection
def get_tickets_from_db_by_status(ticket_status,conn=None):
    """Gets all tickets of a given status (as an INT) and returns a list of Ticket objects"""
    get_ticket_sql = """SELECT ticket_id,
	                           ticket_name,
	                           ticket_requestor,
	                           ticket_date,
	                           ticket_status,
	                           ticket_creature_a,
	                           ticket_creature_b,
	                           ticket_pups,
                               users.user_id,
	                           users.user_level,
	                           users.user_wallet,
	                           users.user_lastbreed,
	                           users.user_warnings_issued,
	                           users.user_pending_breeding,
	                           creature_a.creature_name,
                               creature_a.creature_owner,
                               creature_a.creature_id,
	                           creature_a.creature_create_date,
	                           creature_a.creature_image_link,
                               creature_a.creature_image_link_newborn,
                               creature_a.creature_image_link_pup,
	                           creature_a.creature_generation,
	                           creature_a.creature_traits,
	                           creature_a.creature_parent_a,
	                           creature_a.creature_parent_b,
	                           creature_a.creature_available_to_breed,
                               creature_a.creature_is_active,
                               creature_a.creature_last_forage,
	                           creature_b.creature_name as b_creature_name,
                               creature_b.creature_owner as b_owner,
                               creature_b.creature_id as b_creature_id,
	                           creature_b.creature_create_date as b_create_date,
	                           creature_b.creature_image_link as b_image_link,
                               creature_b.creature_image_link_newborn as b_newborn,
                               creature_b.creature_image_link_pup as b_pup,
	                           creature_b.creature_generation as b_generation,
	                           creature_b.creature_traits as b_traits,
	                           creature_b.creature_parent_a as b_parent_a,
	                           creature_b.creature_parent_b as b_parent_b,
	                           creature_b.creature_available_to_breed as b_available_to_breed,
                               creature_b.creature_is_active as b_is_active,
                               creature_b.creature_last_forage as b_last_forage
	                    FROM breeding_tickets
	                    JOIN users ON breeding_tickets.ticket_requestor = users.user_id
	                    JOIN creatures creature_a on breeding_tickets.ticket_creature_a = creature_a.creature_id
	                    JOIN creatures creature_b on breeding_tickets.ticket_creature_b = creature_b.creature_id
	                    WHERE breeding_tickets.ticket_status = %s
	                    ORDER BY ticket_id ASC"""
    cur = conn.cursor()
    cur.execute(get_ticket_sql,(Constants.TICKET_STATUS[ticket_status],))
    result = cur.fetchall()
    if result:
        returned_tickets = []
        for result_row in result:
            ticket = result_row[:8]
            requestor_result = result_row[8:14]
            creature_a_result = result_row[14:28]
            creature_b_result = result_row[28:]
            requestor = pack_user(requestor_result)
            tkt_creature_a = pack_creature(creature_a_result)
            tkt_creature_b = pack_creature(creature_b_result)
            tkt_pups = pickle.loads(ticket[7])
            returned_ticket =Ticket(
                ticket_name = ticket[1],
                ticket_requestor = requestor,
                creature_a = tkt_creature_a,
                creature_b = tkt_creature_b,
                ticket_id=ticket[0],
                ticket_date=ticket[3],
                ticket_status=ticket[4],
            pups = tkt_pups)
            returned_tickets.append(returned_ticket)
        return returned_tickets
    return None

@make_database_connection
def update_ticket_status(ticket_to_update,conn=None):
    """Advances"""
    update_status_sql = """UPDATE breeding_tickets
                            SET ticket_status=%s
                            WHERE ticket_id=%s"""
    cur = conn.cursor()
    cur.execute(update_status_sql,(ticket_to_update.status,ticket_to_update.id))
    conn.commit()
    return True

@make_database_connection
def update_ticket_in_db(ticket,conn=None):
    """Updates ticket fields after a deferred breeding is accepted."""
    update_ticket_sql = """UPDATE breeding_tickets
                        SET ticket_name=%s,
                            ticket_status=%s,
                            ticket_pups=%s
                        WHERE ticket_id=%s"""
    pickled_pups = pickle.dumps(ticket.pups)
    cur = conn.cursor()
    cur.execute(update_ticket_sql,(ticket.name,
                                   ticket.status,
                                   pickled_pups,
                                   ticket.id))
    conn.commit()
    return True

@make_database_connection
def get_my_tickets_from_db(user_id,conn=None):
    """Gets all tickets that match a given user_id and returns a
    tuple of tuples representing each row"""
    get_tickets_sql = """SELECT ticket_id,
                                ticket_name,
                                ticket_status
                         FROM breeding_tickets
                         WHERE ticket_requestor = %s"""
    cur = conn.cursor()
    cur.execute(get_tickets_sql,(user_id,))
    returned_rows = cur.fetchall()
    if returned_rows:
        return returned_rows
    return None

@make_database_connection
def delete_ticket(ticket_id,conn=None):
    """Deletes a ticket from the breeding_tickets db"""
    delete_ticket_sql = """DELETE FROM breeding_tickets WHERE ticket_id = %s"""
    cur = conn.cursor()
    cur.execute(delete_ticket_sql,(ticket_id,))
    conn.commit()
    if cur.rowcount == 1:
        return True
    return False

@make_database_connection
def get_requested_tickets_from_db(type_to_show,conn=None):
    """Retreives all tickets from the breeding_tickets and returns a
    tuple of tuples representing each row.  Query depends on argument"""
    options={}
    options['open']="""SELECT ticket_id,
                              ticket_name,
                              ticket_status
                        FROM breeding_tickets
                        WHERE ticket_status != 'Complete'
                        ORDER BY ticket_id ASC"""
    options['pending']="""SELECT ticket_id,
                              ticket_name,
                              ticket_status
                        FROM breeding_tickets
                        WHERE ticket_status = 'Breeding Pending'
                        ORDER BY ticket_id ASC"""
    options['ready']="""SELECT ticket_id,
                               ticket_name,
                               ticket_status
                        FROM breeding_tickets
                        WHERE ticket_status = 'Ready to Birth'
                        ORDER BY ticket_id ASC"""
    cur = conn.cursor()
    cur.execute(options[type_to_show])
    returned_rows = cur.fetchall()
    if returned_rows:
        return returned_rows
    return None

@make_database_connection
def get_active_creatures_for_user(user_id,conn=None):
    """Retrieves all creatures that are active for a given user
    
    Parameters
    ----------
    user_id: int
        the user_id to query for"""
    get_creatures_sql="""SELECT creature_id,creature_name FROM creatures
                         WHERE creature_owner = %s AND creature_is_active = TRUE"""
    cur = conn.cursor()
    cur.execute(get_creatures_sql,(user_id,))
    result = cur.fetchall()
    return result or None

def pack_creature(returned_row):
    returned_creature = Creature(name=returned_row[0],
                                     owner=returned_row[1],
                                     creatureId=returned_row[2],
                                     createDate=returned_row[3],
                                     imageLink=returned_row[4],
                                     imageLink_nb=returned_row[5],
                                     imageLink_pup=returned_row[6],
                                     generation=returned_row[7],
                                     available_to_breed=returned_row[11],
                                     is_active=returned_row[12],
                                     last_forage=returned_row[13])
    if returned_row[8]:
        returned_creature.traits=pickle.loads(returned_row[8])
    if returned_row[9] or returned_row[10]:
        returned_creature.parents = [returned_row[9],returned_row[10]]
    return returned_creature

def pack_user(user_data):
    return User(userId = user_data[0],
                level=user_data[1],
                wallet=user_data[2],
                lastBreed=user_data[3],
                warningsIssued=user_data[4],
                is_breeding_pending=user_data[5])

if __name__ == "__main__":
    new_name = "Renamed Creature"
    test_creature = get_creature_from_db(57)
    test_creature.name=new_name
    update_creature(test_creature)
