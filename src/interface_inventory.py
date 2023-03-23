from datetime import datetime
import database_methods
from data import item_effects
import support_functions

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
    user_inventory = database_methods.get_user_inventory(user_id)
    try:
        ids_in_inventory = [row[0] for row in user_inventory]
    except TypeError:
        ids_in_inventory = []
    print(item_id)
    print(ids_in_inventory)
    if int(item_id) in ids_in_inventory:
        item_to_use = database_methods.get_item_from_db(item_id)
        item_to_use = get_item_effect(item_to_use)
        print(item_to_use.name)
        try:
            msg = item_to_use.activate(user_id)
            database_methods.remove_item_from_user(user_id,item_id)
        except TypeError as e:
            print(e)
            msg = 'This item cannot be used'
    else:
        msg = 'Item could not be found in your inventory'
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

if __name__ == '__main__':
    test_user = database_methods.get_user_from_db(99)
    test_user.lastBreed = datetime.today()
    database_methods.update_user_last_breed(test_user)
    #print(use_item_from_inventory(30,99))
