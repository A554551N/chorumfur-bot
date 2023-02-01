from discord.ext import commands
from Creature import Creature
from Item import Item
import database_methods
import support_functions

def is_guild_owner_or_bot_admin():
    """Checks to see if the author of a message is guild_owner or bot creator"""
    def predicate(ctx):
        # removing ctx.guild is not None here would allow DMing admin commands to bot
        return ctx.guild is not None and (ctx.guild.owner_id == ctx.author.id or ctx.author.id == 202632427535859712)
    return commands.check(predicate)

class AdminCog(commands.GroupCog, name='Admin Tools', group_name='admin'):
    """Cog to group commands accessible only to admins"""

    def __init__(self, bot):
        self.client = bot

    @commands.command()
    @is_guild_owner_or_bot_admin()
    async def makeCreature(self,ctx,creature_name,main_horn_trait,
                                       cheek_horn_trait,
                                       face_horn_trait,
                                       tail_trait,
                                       tail_tip_trait,
                                       fluff_trait,
                                       mutation_trait,
                                       owner = None):
        """ADMIN COMMAND: Adds a creature to the database with specific traits"""
        if owner is None:
            owner_id = ctx.message.author.id
        else:
            owner_id = support_functions.strip_mention_format(owner)
        creature_to_add = Creature(name = creature_name,
                                      owner = owner_id,
                                      traits={
                                        'MAIN_HORN':main_horn_trait,
                                        'CHEEK_HORN':cheek_horn_trait,
                                        'FACE_HORN':face_horn_trait,
                                        'TAIL':tail_trait,
                                        'TAIL_TIP':tail_tip_trait,
                                        'FLUFF': fluff_trait,
                                        'MUTATION': mutation_trait
                                      })
        creature_id = database_methods.add_creature_to_db(creature_to_add)
        msg=f"{creature_name} created with Id #{creature_id}"
        await ctx.send(msg)

    @commands.command()
    @is_guild_owner_or_bot_admin()
    async def makeRandomCreature(self,ctx,creatureName):
        """Takes in a creature name and stores a creature with that name in the database
        with randomized traits.  Outputs the creature to the interface after completion."""
        user_id = ctx.message.author.id
        creature_to_add = Creature(creatureName,user_id)
        creature_to_add.randomize_creature()
        creature_id = database_methods.add_creature_to_db(creature_to_add)
        if creature_id:
            creature_to_add.creatureId=creature_id
            await ctx.send(f"{creatureName} added to database with ID #{creature_id}")
            await ctx.send(creature_to_add.outputCreature()[0])
        else:
            await ctx.send(f"An error occurred adding {creatureName} to the database")

    @commands.command()
    @is_guild_owner_or_bot_admin()
    async def makeItem(self,ctx,item_name,item_desc,item_value):
        """Takes in a name, description, and value and stores a new item in the items database."""
        if ctx.message.attachments:
            image_link = ctx.message.attachments[0].url
        else:
            image_link = ""
        item_to_add = Item(item_name,item_desc,item_value,image_link)
        item_id = database_methods.add_item_to_db(item_to_add)
        if item_id:
            await ctx.send(f'{item_name} created with ID # {item_id}')
        else:
            await ctx.send(f'{item_name} cannot be created, an error occurred.')

    @commands.command()
    @is_guild_owner_or_bot_admin()
    async def getAllItems(self,ctx):
        """Retrieves all items defined in the items database and displays them as a list."""
        output = "**Item ID | Item Name - Item Value**\n```"
        for item in database_methods.get_all_items_from_db():
            output+= f"{item[0]} | {item[1]} - {item[2]}\n"
        output+= "```**For more information run `.getItem <Item ID>`**"
        await ctx.send(output)

    @commands.command()
    @is_guild_owner_or_bot_admin()
    async def addItemToInv(self,ctx,item_id_to_add,user_id = None,quantity=1):
        """adds an item to a given users inventory with a given quantity.
        If no user ID is specified, items will be given to the user who invoked the command.
        If a quantity is not specified, it will add 1."""
        if user_id is None:
            user_id = ctx.message.author.id
        if database_methods.add_item_to_user(user_id,item_id_to_add,quantity):
            await ctx.send("Inventory update successful.")
        else:
            await ctx.send("Inventory update failed.")

    @commands.command()
    @is_guild_owner_or_bot_admin()
    async def removeItemFromInv(self,ctx,item_id_to_remove,user_id = None,quantity=1):
        """ADMIN COMMAND: Removes a given quantity of an item from a given user's inventory.
        If no user is specified, removes an item from your own inventory.
        If no quantity is specified, removes 1."""
        if user_id is None:
            user_id = ctx.message.author.id
        if database_methods.remove_item_from_user(user_id,item_id_to_remove,quantity):
            await ctx.send("Item removed from User Inventory")
        else:
            await ctx.send("Item not found, or not successfully removed.")

async def setup(bot):
    await bot.add_cog(AdminCog(bot))
