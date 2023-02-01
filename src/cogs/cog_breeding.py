from discord.ext import commands
from Ticket import Ticket
from ConstantData import Constants
import database_methods

class BreedingCog(commands.GroupCog, name='Breeding',group_name='breeding'):
    """Cog to group commands related to breeding"""
    def __init__(self,bot):
        self.client = bot

    async def send_ticket_to_channel(self,ticket):
        """Sends a message to the tickets channel and mentions artist"""
        artist = self.client.get_user(101509826588205056)
        ticket_channel = self.client.get_channel(1061868480086941716)
        await ticket_channel.send(artist.mention)
        await ticket_channel.send(ticket.output_detailed_ticket())

    def add_pups_to_database(self,ticket):
        """Iterates over the pups parameter of a ticket object and adds them to database."""
        for pup in ticket.pups:
            pup.creatureId = database_methods.add_creature_to_db(pup)
        return ticket

    def enact_breeding(self,ticket):
        """Performs the core logic of breeding based on a supplied Ticket object.
    Returns the updated Ticket object"""
        ticket.update_ticket_status(3)
        ticket.requestor.update_last_breed()
        database_methods.update_user_last_breed(ticket.requestor)
        ticket.perform_breeding()
        ticket = self.add_pups_to_database(ticket)
        return ticket

    def create_breeding_ticket(self,requesting_user_id,creature_a_id,creature_b_id):
        """Takes in a user ID and two creature IDs and returns a breeding Ticket"""
        requesting_user = database_methods.get_user_from_db(requesting_user_id)
        creature_a=database_methods.get_creature_from_db(creature_a_id)
        creature_b=database_methods.get_creature_from_db(creature_b_id)
        parents_of_a=database_methods.get_parents_from_db(creature_a)
        parents_of_b=database_methods.get_parents_from_db(creature_b)
        return Ticket(ticket_name=f"{creature_a.name} x {creature_b.name}",
                           ticket_requestor=requesting_user,
                           creature_a=creature_a,
                           creature_b=creature_b,
                           parents_of_a=parents_of_a,
                           parents_of_b=parents_of_b)

    async def pend_breeding(self,ctx,ticket):
        """Creates a Ticket in a Pending state and submits the information to the
     pending_breedings channel.  Returns the modified Ticket."""
        ticket.update_ticket_status(2)
        ticket.id = database_methods.add_ticket_to_db(ticket)
        pending_breedings = self.client.get_channel(1067121489444339844)
        other_user = self.client.get_user(ticket.other_user())
        await pending_breedings.send(
            f"{other_user.mention}: Please use .accept "\
            f"{ticket.id} to confirm the following breeding, or "\
            f".decline {ticket.id} to reject it.  Unanswered tickets"\
            " will expire after 30 days.\n"\
            f"{ticket.output_ticket()}")
        await ctx.send(f"Ticket #{ticket.id} has been submitted for "\
                       f"breeding with a status of {ticket.status}")

    @commands.command()
    async def breed(self,ctx,creature_a_id,creature_b_id):
        """Submit a breeding request in format .breed <creature_a> <creature_b>"""
        breed_request=self.create_breeding_ticket(requesting_user_id=ctx.message.author.id,
                                                  creature_a_id=creature_a_id,
                                                  creature_b_id=creature_b_id)
        if breed_request.requestor_can_breed():
            if breed_request.requestor_owns_both():
                breed_request = self.enact_breeding(breed_request)
                breed_request.id = database_methods.add_ticket_to_db(breed_request)
                await self.send_ticket_to_channel(breed_request)
                await ctx.send("Breeding has been successfully submitted.  "\
                              f"Your Ticket # is {breed_request.id}")
            else:
                await self.pend_breeding(ctx,breed_request)
        else:
            await ctx.send("Breeding request was not able to be submitted at this time."\
                " Please confirm you own at least one of the creatures submitted "\
                "and that your breeding crystal is fully charged.")

    @commands.command(aliases=['accept'])
    async def acceptBreeding(self,ctx,ticket_id):
        """.acceptBreeding <ticket_id> moves a ticket from pending state to active and
        performs the breeding."""
        ticket = database_methods.get_ticket_from_db(ticket_id)
        if ticket.other_user() != ctx.message.author.id:
            msg = "You do not have permission to modify this ticket."
        elif ticket.status != Constants.TICKET_STATUS[2]:
            msg = f"This ticket is in {ticket.status} and cannot be modified."
        else:
            ticket = self.enact_breeding(ticket)
            database_methods.update_ticket_in_db(ticket)
            await self.send_ticket_to_channel(ticket)
            msg = f"Ticket {ticket.id} has been accepted.  Status is now {ticket.status}"
        await ctx.send(msg)

    @commands.command(aliases=['decline'])
    async def declineBreeding(self,ctx,ticket_id):
        """.declineBreeding <ticket_id> moves a ticket from pending state to cancelled."""
        ticket = database_methods.get_ticket_from_db(ticket_id)
        if ticket.other_user() != ctx.message.author.id:
            msg = "You do not have permission to modify this ticket."
        elif ticket.status != Constants.TICKET_STATUS[2]:
            msg = f"This ticket is in {ticket.status} and cannot be modified."
        else:
            ticket.update_ticket_status(6)
            database_methods.update_ticket_in_db(ticket)
            msg = f"Ticket {ticket.id} has been rejected.  Status is now {ticket.status}"
        await ctx.send(msg)

async def setup(bot):
    await bot.add_cog(BreedingCog(bot))
