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

    @commands.command(aliases=['gc','getcreature'],require_var_positional=True)
    async def getCreature(self,ctx,creatureId):
        """Takes in a creature ID and sends a formatted output of the creature to discord"""
        requested_creature = database_methods.get_creature_from_db(creatureId)
        if requested_creature:
            user = self.client.get_user(requested_creature.owner)
            requested_creature.ownerName = user.name
            returned_values = requested_creature.outputCreature()
            await ctx.send(returned_values[0])
            await ctx.send(returned_values[1])
        else:
            await ctx.send(f"ID Number {creatureId} not found")

    @commands.command()
    async def inventory(self,ctx):
        """Displays a user's inventory"""
        await ctx.send(f"Fetching Inventory {ctx.message.author.mention}")
        user = database_methods.get_user_from_db(ctx.message.author.id)
        await ctx.send(user.outputInventory())
        await ctx.send("For more information on an item, use .getItem <ID Number>")

async def setup(bot):
    await bot.add_cog(GetGroupCog(bot))
