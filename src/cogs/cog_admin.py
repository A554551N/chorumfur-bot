from discord.ext import commands
import database_methods

class AdminCog(commands.GroupCog, name='Admin Tools',group_name='admin'):
    """Cog to group commands accessible only to admins"""
    def __init__(self,bot):
        self.client = bot

async def setup(bot):
    await bot.add_cog(AdminCog(bot))
