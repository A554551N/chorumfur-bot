from discord.ext import commands
import database_methods

class CreaturesCog(commands.GroupCog, name='Chorumfur Management',group_name='chorumfurs'):
    """Cog to group commands related to managing creatures"""
    def __init__(self,bot):
        self.client = bot

async def setup(bot):
    await bot.add_cog(CreaturesCog(bot))
