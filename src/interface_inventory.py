from datetime import datetime
import database_methods
from data import item_effects
import support_functions
from collections import namedtuple


def get_item(item_id):
    """Get an item from the database by item ID and returns
     the appropriate Item object to the Bot
    
    Parameters
    ------------
    item_id : int
        an int corresponding to a DB item ID"""
    return database_methods.get_item_from_db(item_id)

def get_inventory(user_id):
    """Gets all of a users items and returns it as a list of messages.
    
    Parameters
    -----------
    user_id : int
        The ID of the user who invoked the command"""

    returned_inventory =  database_methods.get_user_inventory(user_id) or None
    if returned_inventory:
        msg_list = support_functions.format_output("{} - {} - {}\n",
                                                  ("ID#","Item Name","Quantity"),
                                                  returned_inventory)
        msg_list.append("**For more information on an item, use `.getItem <ID Number>`**")
        return msg_list
    else:

        return ["No Items Found"]

def use_item_from_inventory(item_id,user_id,target_id=None):
    """performs the action of an inventory item and removes it from the user's inventory.
    Returns a message for the bot to display

    Parameters
    ----------
    item_id : int
        The ID of the item to use
    user_id : int
        The ID of the user who invoked the command
    """
    msg = ""
    try:
        user_inventory = format_inventory(database_methods.get_user_inventory(user_id))
    except TypeError:
        user_inventory = []
    if item_id in user_inventory:
        item_to_use = database_methods.get_item_from_db(item_id)
        item_to_use = get_item_effect(item_to_use)
        try:
            msg = item_to_use.activate(user_id=user_id,target_id=target_id,item=item_to_use)
            database_methods.remove_item_from_user(user_id,item_id)
        except TypeError:
            msg = (None,'This item cannot be used')
    else:
        msg = (None,'Item could not be found in your inventory')
    return msg

def get_item_effect(item_to_get):
    """Inserts the item's activation method and returns the completed
    object.
    
    Parameters
    ----------
    item_to_get : Item
        the item that needs its activation"""

    if item_to_get.id in item_effects.items:
        item_to_get.activate = item_effects.items[item_to_get.id]
    else:
        item_to_get.activate = None
    return item_to_get

def give_item(giver_id,receiver_id,item_id,qty):
    """Removes a given quantity of an item from one user's inventory and adds
    it to another user's inventory.  Returns a message for the bot to display.
    
    Parameters
    ----------
    giver_id : int
        The giver's user ID
    receiver : string
        The receiver's @mention formatted username
    item_id : int
        The item to transfer
    qty : int
        The quantity of items to transfer
    """
    item_id = int(item_id)
    giver_inventory = format_inventory(database_methods.get_user_inventory(giver_id))
    if item_id in giver_inventory:
        if giver_inventory[item_id].quantity >= qty:
            database_methods.remove_item_from_user(giver_id,item_id,qty)
            database_methods.add_item_to_user(receiver_id,item_id,qty)
            return "Items have been successfully transferred."
    return "Items could not be transferred."

def format_inventory(user_inventory):
    """Takes in a user's inventory and returns a dictionary containing the items in the inventory
    as Item objects
    
    Parameters
    ---------
    user_inventory : tuple
        a user's inventory supplied by database_methods.get_user_inventory()"""
    inventory_dict = {}
    InventoryItem = namedtuple("Item","name quantity")
    for row in user_inventory:
        inventory_dict[row[0]] = InventoryItem(row[1],row[2])
    return inventory_dict

if __name__ == '__main__':
    test_user = database_methods.get_user_from_db(99)
    test_user.lastBreed = datetime.today()
    database_methods.update_user_last_breed(test_user)
    #print(use_item_from_inventory(30,99))
