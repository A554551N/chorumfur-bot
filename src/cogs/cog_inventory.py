import interface_inventory
from discord.ext import commands

class InventoryCog(commands.GroupCog, name='Inventory Management',group_name='inventory'):
    """Cog to group commands related to managing inventory"""
    def __init__(self,bot):
        self.client = bot

    @commands.command()
    async def getItem(self,ctx,item_id):
        """Displays details of a given Item ID"""
        item=interface_inventory.get_item(item_id)
        await ctx.send(f"{ctx.message.author.mention}\n{item.outputItem()}")
        if item.imageLink is not None:
            await ctx.send(item.imageLink)
    
    @commands.command()
    async def inventory(self,ctx):
        """Displays a user's inventory"""
        msg_list = interface_inventory.get_inventory(ctx.message.author.id)
        for msg in msg_list:
            await ctx.send(msg)

    @commands.command()
    async def useItem(self,ctx,item_id,target=None):
        """Consumes an item from the user's inventory and performs its effect
        
        Parameters
        ----------
        item_id : int
            item to use"""

        msg_list = []
        msg_list.append(interface_inventory.use_item_from_inventory(item_id,ctx.message.author.id,target))
        for msg in msg_list:
            await ctx.send(msg)

async def setup(bot):
    await bot.add_cog(InventoryCog(bot))
