from discord.ext import commands
import database_methods

class GetGroupCog(commands.GroupCog, name='Get',group_name='get'):
    """Cog to group 'get' commands (ie GET creature,item,ticket,etc)"""
    def __init__(self,bot):
        self.client = bot

    @commands.command(name='me')
    async def get_own_user_details(self,ctx):
        """gets user profile and displays it in chat"""
        user = database_methods.get_user_from_db(ctx.message.author.id)
        if user:
            user.name = self.client.get_user(ctx.message.author.id)
            msg = f"{ctx.message.author.mention}\n{user.outputProfile()}"
        else:
            msg = "A profile was not found for you.  If you haven't use .joinGame"
        await ctx.send(msg)

async def setup(bot):
    await bot.add_cog(GetGroupCog(bot))
