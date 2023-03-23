import database_methods
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

def use_item_from_inventory(item_id,user_id):
    """performs the action of an inventory item and removes it from the user's inventory.
    Returns a list of messages for the bot to display

    Parameters
    ----------
    item_id : int
        The ID of the item to use
    user_id : int
        The ID of the user who invoked the command
    """
    msg_list = []
    user_inventory = database_methods.get_user_inventory(user_id)
    ids_in_inventory = [row[0] for row in user_inventory]
    if item_id in ids_in_inventory:
        item_to_use = database_methods.get_item_from_db(item_id)
        msg_list.append(item_to_use.activate())
        database_methods.remove_item_from_user(user_id,item_id)
    else:
        msg_list.append('Item could not be found in your inventory')
    return msg_list

if __name__ == '__main__':
    print(use_item_from_inventory(99999,99))
