import interface_inventory
import support_functions
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
    async def giveItem(self,ctx,item_id,recipient,quantity=1):
        giver_id = ctx.message.author.id
        recipient_id = support_functions.strip_mention_format(recipient)
        msg_list = []
        msg_list.append(interface_inventory.give_item(giver_id,recipient_id,item_id,quantity))
        for msg in msg_list:
            await ctx.send(msg)

    @commands.command()
    async def useItem(self,ctx,item_id,target=None):
        """Uses a consumable item from a user's inventory."""
        user_id = ctx.message.author.id
        msg_list = []
        msg_list.append(interface_inventory.use_item_from_inventory(int(item_id),user_id,target))
        for msg in msg_list:
            if msg[0] == 'ticket':
                await support_functions.send_ticket_to_channel(self.client,msg[2])
                await ctx.send(msg[1])
            else:
                await ctx.send(msg[1])

async def setup(bot):
    await bot.add_cog(InventoryCog(bot))
