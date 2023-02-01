from discord.ext import commands
import database_methods

class BreedingCog(commands.GroupCog, name='Breeding',group_name='breeding'):
    """Cog to group commands related to breeding"""
    def __init__(self,bot):
        self.client = bot

async def setup(bot):
    await bot.add_cog(BreedingCog(bot))
