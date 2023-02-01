"""Contains support methods shared by cog_breeding and cog_admin"""
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


def enact_breeding(ticket):
    """Performs the core logic of breeding based on a supplied Ticket object.
Returns the updated Ticket object"""
    ticket.update_ticket_status(3)
    ticket.requestor.update_last_breed()
    database_methods.update_user_last_breed(ticket.requestor)
    ticket.perform_breeding()
    ticket = add_pups_to_database(ticket)
    return ticket


def add_pups_to_database(ticket):
    """Iterates over the pups parameter of a ticket object and adds them to database."""
    for pup in ticket.pups:
        pup.creatureId = database_methods.add_creature_to_db(pup)
    return ticket


async def send_ticket_to_channel(bot,ticket):
    """Sends a message to the tickets channel and mentions artist"""
    artist = bot.get_user(101509826588205056)
    ticket_channel = bot.get_channel(1061868480086941716)
    await ticket_channel.send(artist.mention)
    await ticket_channel.send(ticket.output_detailed_ticket())
