from discord.ext import commands
import database_methods

class InventoryCog(commands.GroupCog, name='Inventory Management',group_name='inventory'):
    """Cog to group commands related to managing inventory"""
    def __init__(self,bot):
        self.client = bot

async def setup(bot):
    await bot.add_cog(InventoryCog(bot))
