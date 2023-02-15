import database_methods
import support_functions
from discord.ext import commands
from ConstantData import Constants


class TicketCog(commands.GroupCog, name='Ticket Management',group_name='tickets'):
    """Cog to group commands related to managing Tickets"""
    def __init__(self,bot):
        self.client = bot

    @commands.command(aliases=['gt'])
    async def getTicket(self,ctx,ticket_id):
        """Retreives a ticket from the database by ID number and displays a summary."""
        returned_ticket = database_methods.get_ticket_from_db(ticket_id)
        await ctx.send(returned_ticket.output_ticket())

    @commands.command()
    async def cancelTicket(self,ctx,ticket_id):
        """Cancels an in progress pairing ticket"""
        ticket = database_methods.get_ticket_from_db(ticket_id)
        if ctx.message.author.id != ticket.requestor.userId:
            msg = "You do not have permission to modify this ticket."
        elif ticket.status in (Constants.TICKET_STATUS[5],Constants.TICKET_STATUS[6]):
            msg = "You cannot cancel a completed ticket."
        else:
            if database_methods.delete_ticket(ticket_id):
                msg = "Your ticket has been successfully removed from the database."
                tickets_channel = self.client.get_channel(1061868480086941716)
                artist = self.client.get_user(101509826588205056)
                await tickets_channel.send(f"{artist.mention} **User has requested cancellation"\
                                f"of ticket #{ticket.id}**")
            else:
                msg="An error occurred deleting your ticket from the database."
        await ctx.send(msg)

    @commands.command(aliases=['mt'])
    async def myTickets(self,ctx):
        """Retreives all tickets that belong to the user and displays them in a list"""
        user_id = ctx.message.author.id
        returned_tickets = database_methods.get_my_tickets_from_db(user_id) or None
        if returned_tickets:
            msg_list = support_functions.format_output("{} - {} - {}\n",
                                                       ("ID#","Ticket Name", "Status"),
                                                       returned_tickets)
            for msg in msg_list:
                await ctx.send(msg)
            await ctx.send("**For more information run `.getTicket <ticket ID>`**")
        else:
            await ctx.send("No Tickets Found")

async def setup(bot):
    await bot.add_cog(TicketCog(bot))
