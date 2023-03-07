"""Contains support methods shared by cog_breeding and cog_admin"""
from random import random
from decimal import Decimal
from Ticket import Ticket
import database_methods


def create_breeding_ticket(requesting_user_id, creature_a_id, creature_b_id):
    """Takes in a user ID and two creature IDs and returns a breeding Ticket"""
    requesting_user = database_methods.get_user_from_db(requesting_user_id)
    creature_a = database_methods.get_creature_from_db(creature_a_id)
    creature_b = database_methods.get_creature_from_db(creature_b_id)
    parents_of_a = database_methods.get_parents_from_db(creature_a)
    parents_of_b = database_methods.get_parents_from_db(creature_b)
    return Ticket(ticket_name=f"{creature_a.name} x {creature_b.name}",
                  ticket_requestor=requesting_user,
                  creature_a=creature_a,
                  creature_b=creature_b,
                  parents_of_a=parents_of_a,
                  parents_of_b=parents_of_b)


def enact_breeding(ticket,is_admin=False):
    """Performs the core logic of breeding based on a supplied Ticket object.
Returns the updated Ticket object"""
    ticket.update_ticket_status(3)
    if not is_admin:
        ticket.requestor.update_last_breed()
        database_methods.update_user_last_breed(ticket.requestor)
    pups = ticket.perform_breeding()
    ticket.pups = database_methods.add_multiple_creatures_to_db(pups)
    return ticket

async def send_ticket_to_channel(bot, ticket):
    """Sends a message to the tickets channel and mentions artist"""
    artist = bot.get_user(101509826588205056)
    ticket_channel = bot.get_channel(1061868480086941716)
    pups = database_methods.get_multiple_creatures_from_db(ticket.pups)
    await ticket_channel.send(artist.mention)
    await ticket_channel.send(ticket.output_detailed_ticket(pups))

def format_output(format_str,header_elements,returned_list_from_db):
    """Takes in a format string, the elements that form the header,
     a list taken from the db and returns a list of formatted string
     suitable for use in list-style outputs
     
    Parameters
    ----------
    format_str : str
        string formatted as '{} - {}\n' with appropriate # of slots
    header_elements : tuple
        tuple containing all header elements
    returned_list_from_db : tuple
        a tuple containing all of the returned records from the db
    """
    
    # PAD THE CELLS TO KEEP THE LINES STRAIGHT
    output_len = 0 # counts characters
    msg_list = [] # the list of messages to return
    msg_count = 0
    header = format_str.format(*header_elements)
    msg_list.append(f"**{header}**```")
    for row in returned_list_from_db:
        output_str = format_str.format(*row)
        output_len += len(output_str)
        if output_len > 1900:
            msg_list[msg_count] += "```"
            msg_count += 1
            output_len = 0
        if output_len==0:
            msg_list.append(f"**{header}**```")
        msg_list[msg_count] += output_str
    msg_list[msg_count] +="```"
    return msg_list

def strip_mention_format(mention):
    """removes leading <@ and trailing > from user IDs passed as mentions"""
    return mention[2:-1]

def roll_random_result(dict_to_roll):
    """Takes in a dict of outcomes (keys) and decimal weights in string format (values)
    and returns one selected randomly while respecting weights.
    
    Parameters
    ----------
    dict_to_roll: dict
        The dictionary containing the possible results"""
    random_result = Decimal(random())
    sum_of_options = 0
    for weight in dict_to_roll.values():
        sum_of_options += Decimal(weight)
    if sum_of_options != 1:
        return None
    for outcome in dict_to_roll:
        weight = Decimal(dict_to_roll[outcome])
        if random_result > weight:
            random_result -= weight
        else:
            return outcome
