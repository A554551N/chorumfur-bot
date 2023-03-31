"""Contains the activation effects for all items in game and a dictionary to reference them."""
import database_methods

def item_99999_effect(target_arg):
    """Effect of item 99999, Test Item"""
    return "Item Used Successfully"

def crystal_reset_effect(user_id):

    """Effect of item 30, Mating Reset
    This item will reset a user's mating crystal so they can mate again immediately"""
    user_to_reset = database_methods.get_user_from_db(user_id)
    user_to_reset.lastBreed = None
    database_methods.update_user_last_breed(user_to_reset)
    return "The magic of the crystal is spent and your mating crystal is full again!"

items = {
    30 : crystal_reset_effect,
    99999 : item_99999_effect
}
