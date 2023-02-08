import database_methods
import support_functions
from discord.ext import commands

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
        returned_inventory = database_methods.get_user_inventory(ctx.message.author.id) or None
        if returned_inventory:
            msg_list = support_functions.format_output("{} - {} - {}\n",
                                                       ("ID#","Item Name","Quantity"),
                                                       returned_inventory)
            for msg in msg_list:
                await ctx.send(msg)
            await ctx.send("**For more information on an item, use `.getItem <ID Number>`**")
        else:
            await ctx.send("No Items Found")


async def setup(bot):
    await bot.add_cog(InventoryCog(bot))
