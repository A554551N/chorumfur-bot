from discord.ext import commands
import database_methods

class TicketCog(commands.GroupCog, name='Ticket Management',group_name='tickets'):
    """Cog to group commands related to managing Tickets"""
    def __init__(self,bot):
        self.client = bot

async def setup(bot):
    await bot.add_cog(TicketCog(bot))
