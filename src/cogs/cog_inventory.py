from discord.ext import commands
import database_methods

class InventoryCog(commands.GroupCog, name='Inventory Management',group_name='inventory'):
    """Cog to group commands related to managing inventory"""
    def __init__(self,bot):
        self.client = bot

    @commands.command()
    async def getItem(self,ctx,item_id):
        """Displays details of a given Item ID"""
        item=database_methods.get_item_from_db(item_id)
        await ctx.send(f"{ctx.message.author.mention}\n{item.outputItem()}")
        if item.imageLink is not None:
            await ctx.send(item.imageLink)
    
    @commands.command()
    async def inventory(self,ctx):
        """Displays a user's inventory"""
        await ctx.send(f"Fetching Inventory {ctx.message.author.mention}")
        user = database_methods.get_user_from_db(ctx.message.author.id)
        await ctx.send(user.outputInventory())
        await ctx.send("For more information on an item, use .getItem <ID Number>")


async def setup(bot):
    await bot.add_cog(InventoryCog(bot))
