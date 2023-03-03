from discord.ext import commands
from ConstantData import Constants
from User import User
import database_methods


class UserCog(commands.GroupCog, name='User Management', group_name='users'):
    """Cog to group commands relating to user management"""

    def __init__(self, bot):
        self.client = bot

    @commands.command()
    async def crystal(self, ctx):
        """gets the status of the user's mating crystal and displays it in in chat"""
        user = database_methods.get_user_from_db(ctx.message.author.id)
        if user:
            msg = f"**Last Mating:** {user.lastBreed}\n"\
                f"Crystal Full in {user.daysUntilFull()} days"
        await ctx.send(msg)
        await ctx.send(Constants.CRYSTAL_IMAGE_STAGES[user.breedingLevel()])

    @commands.command(aliases=['join'])
    async def joinGame(self, ctx):
        """Adds a new user to the users database"""
        new_user = User(ctx.message.author.id)
        if database_methods.add_user_to_database(new_user):
            msg = f"Welcome to Chorumfur {self.client.get_user(ctx.message.author.id)}"
        else:
            msg = "Failed to add new user, perhaps you are already registered?  Try .me"
        await ctx.send(msg)

    @commands.command(name='me')
    async def get_own_user_details(self, ctx):
        """gets user profile and displays it in chat"""
        user = database_methods.get_user_from_db(ctx.message.author.id)
        if user:
            user.name = self.client.get_user(ctx.message.author.id)
            msg = f"{ctx.message.author.mention}\n{user.outputProfile()}"
        else:
            msg = "A profile was not found for you.  If you haven't use .joinGame"
        await ctx.send(msg)
    
    @commands.command()
    async def wallet(self,ctx):
        """gets and displays user wallet"""
        user = database_methods.get_user_from_db(ctx.author.id) or None
        if user:
            msg = f"> **{ctx.author.name}'s Wallet:** {user.wallet} baubles"
        else:
            msg = f"No wallet found for {ctx.author.name} or an error has occurred"
        await ctx.send(msg)


async def setup(bot):
    await bot.add_cog(UserCog(bot))
