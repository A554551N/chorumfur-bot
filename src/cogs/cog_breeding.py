import support_functions
from discord.ext import commands
from Ticket import Ticket
from ConstantData import Constants
import database_methods


class BreedingCog(commands.GroupCog, name='Breeding',group_name='breeding'):
    """Cog to group commands related to breeding"""
    def __init__(self,bot):
        self.client = bot


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
        breed_request=support_functions.create_breeding_ticket(requesting_user_id=ctx.message.author.id,
                                                  creature_a_id=creature_a_id,
                                                  creature_b_id=creature_b_id)
        check_result = breed_request.requestor_can_breed()
        if check_result[0]:
            if breed_request.requestor_owns_both():
                breed_request = support_functions.enact_breeding(breed_request)
                breed_request.id = database_methods.add_ticket_to_db(breed_request)
                await support_functions.send_ticket_to_channel(self.client,breed_request)
                await ctx.send("Breeding has been successfully submitted.  "\
                              f"Your Ticket # is {breed_request.id}")
            else:
                await self.pend_breeding(ctx,breed_request)
        else:
            await ctx.send(check_result[1])

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
            ticket = support_functions.enact_breeding(ticket)
            database_methods.update_ticket_in_db(ticket)
            await support_functions.send_ticket_to_channel(self.client,ticket)
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
