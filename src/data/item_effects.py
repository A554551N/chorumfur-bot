"""Contains the activation effects for all items in game and a dictionary to reference them."""
import database_methods
from ConstantData import Constants
from Ticket import Ticket

def item_99999_effect(**kwargs):
    """Effect of item 99999, Test Item"""
    return (None,"Item Used Successfully")

def crystal_reset_effect(**kwargs):
    """Effect of item 30, Mating Reset
    This item will reset a user's mating crystal so they can mate again immediately

    Parameters
    ----------
    user_id : int
        The user ID to reset
    """

    user_to_reset = database_methods.get_user_from_db(kwargs['user_id'])
    user_to_reset.lastBreed = None
    database_methods.update_user_last_breed(user_to_reset)
    return (None,"The magic of the crystal is spent and your mating crystal is full again!")

def palette_rock_effect(**kwargs):
    """Effect of 'palette rock' type items
    This item will submit a ticket requesting an appearance change for the targeted creature.
    Returns a response type of 'ticket' and a message to display
    
    Parameters
    ----------
    user_id : int
        The ID of the user consuming the item
    target_id : int
        The ID of the creature to target with the item
    item : Item
        The Item to consume
    """
    requesting_user = database_methods.get_user_from_db(kwargs['user_id'])
    target_creature = database_methods.get_creature_from_db(kwargs['target_id'])
    palette_item = kwargs['item']
    modification_ticket = Ticket(ticket_name=f'Modify {target_creature.creatureId} - {target_creature.name} with {palette_item.name}',
                                 ticket_requestor=requesting_user,
                                 creature_a=target_creature,
                                 creature_b=None,
                                 ticket_type='modification',
                                 ticket_status=Constants.TICKET_STATUS[3]
                                 )
    modification_ticket.id = database_methods.add_ticket_to_db(modification_ticket)
    if modification_ticket.id:
        return ('ticket',f"Ticket #{modification_ticket.id} has been submitted!",modification_ticket)
    return (None,"Ticket could not be created")

items = {
    30 : crystal_reset_effect,
    31 : palette_rock_effect,
    99999 : item_99999_effect
}
