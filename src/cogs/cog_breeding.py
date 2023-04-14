import support_functions
from discord.ext import commands
from Ticket import Ticket
from ConstantData import Constants
import database_methods


class BreedingCog(commands.GroupCog, name='Mating',group_name='mating'):
    """Cog to group commands related to mating"""
    def __init__(self,bot):
        self.client = bot


    async def pend_breeding(self,ctx,ticket):
        """Creates a Ticket in a Pending state and submits the information to the
     pending_breedings channel.  Returns the modified Ticket."""
        ticket.update_ticket_status(2)
        ticket.id = database_methods.add_ticket_to_db(ticket)
        ticket.requestor.is_breeding_pending = True
        database_methods.update_user_pending_breeding(ticket.requestor)
        pending_breedings = self.client.get_channel(1067121489444339844)
        other_user = self.client.get_user(ticket.other_user())
        await pending_breedings.send(
            f"{other_user.mention}: Please use .accept "\
            f"{ticket.id} to confirm the following pairing, or "\
            f".decline {ticket.id} to reject it.  Unanswered tickets"\
            " will expire after 30 days.\n"\
            f"{ticket.output_ticket()}")
        await ctx.send(f"Ticket #{ticket.id} has been submitted for "\
                       f"mating with a status of {ticket.status}")

    # @commands.command()
    async def mate(self,ctx,creature_a_id,creature_b_id):
        """Submit a mating request in format .mate <creature_a> <creature_b>"""
        breed_request=support_functions.create_breeding_ticket(requesting_user_id=ctx.message.author.id,
                                                  creature_a_id=creature_a_id,
                                                  creature_b_id=creature_b_id)
        check_result = breed_request.requestor_can_breed()
        if check_result[0]:
            if breed_request.requestor_owns_both():
                breed_request = support_functions.enact_breeding(breed_request)
                breed_request.id = database_methods.add_ticket_to_db(breed_request)
                await support_functions.send_ticket_to_channel(self.client,breed_request)
                await ctx.send("Pairing has been successfully submitted.  "\
                              f"Your Ticket # is {breed_request.id}")
            else:
                await self.pend_breeding(ctx,breed_request)
        else:
            await ctx.send(check_result[1])

    @commands.command(aliases=['accept'])
    async def acceptPairing(self,ctx,ticket_id):
        """.acceptPairing <ticket_id> moves a ticket from pending state to active and
        performs the mating."""
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

    @commands.command(aliases=['decline','cancelPairing'])
    async def declinePairing(self,ctx,ticket_id):
        """.declinePairing <ticket_id> moves a ticket from pending state to cancelled."""
        ticket = database_methods.get_ticket_from_db(ticket_id)
        if ctx.message.author.id not in (ticket.requestor.userId,ticket.other_user()):
            msg = "You do not have permission to modify this ticket."
        elif ticket.status != Constants.TICKET_STATUS[2]:
            msg = f"This ticket is in {ticket.status} and cannot be modified."
        else:
            ticket.update_ticket_status(6)
            ticket.requestor.is_breeding_pending = False
            database_methods.update_ticket_in_db(ticket)
            database_methods.update_user_pending_breeding(ticket.requestor)
            msg = f"Ticket {ticket.id} has been rejected.  Status is now {ticket.status}"
            await ctx.send(f"{self.client.get_user(ticket.requestor.userId).mention} "\
                           f"{self.client.get_user(ticket.other_user()).mention}")
        await ctx.send(msg)

    @commands.command()
    async def matingDance(self,ctx,creature_id=None):
        """Checks to see which chorumfurs are doing a mating dance.
        If an owned creature ID is supplied, that creature will stop
        or start doing the mating dance."""
        if creature_id:
            creature = database_methods.get_creature_from_db(creature_id)
            creature.available_to_breed = not creature.available_to_breed
            database_methods.update_creature(creature)
            await ctx.send(f"{creature.name} has {'started' if creature.available_to_breed else 'stopped'}"\
                           " doing the mating dance.")
        else:
            returned_creatures = database_methods.get_creatures_available_to_breed()
            list_of_ids = [creature[0] for creature in returned_creatures]
            largest_id = len(str(max(list_of_ids)))
            padding = max(largest_id - 3,0)
            output=f"**{' '*padding}ID# | Creature Name**\n```"
            for creature in returned_creatures:
                padding = largest_id - len(str(creature[0]))
                output+=f"{' ' * padding}{creature[0]} | {creature[1]}\n"
            output+="```**For more information run `.getCreature <Creature ID>`**"
            await ctx.send(output)


async def setup(bot):
    await bot.add_cog(BreedingCog(bot))
