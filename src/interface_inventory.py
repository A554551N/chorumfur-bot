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