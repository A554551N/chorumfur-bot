import os
import discord
from discord.ext import commands
from Creature import Creature
from User import User
from Item import Item
import database_methods

intents = discord.Intents.default()
intents.message_content = True

game = discord.Game('with all these Chorumfurs!')

client = commands.Bot(command_prefix='.',intents=intents,activity=game)

def is_guild_owner_or_me():
    """Checks to see if the author of a message is guild_owner or bot creator"""
    def predicate(ctx):
        return ctx.guild is not None and (ctx.guild.owner_id == ctx.author.id or ctx.author.id == 202632427535859712)
    return commands.check(predicate)

@client.event
async def on_ready():
    """Called when discord bot is ready to use"""
    print(f'We have logged in as {client.user}')

@client.event
async def on_command_error(ctx, error):
    """Triggers when a command is not processed successfully"""
    print(f"{ctx.message.author}: {error}")
    await ctx.send(f"Command {ctx.message.content} is not recognized or you"\
        " do not have permission to perform this action.")


# BEGIN COMMANDS SECTION
@client.command()
async def shop(ctx):
    """Command triggers the shop interface"""
    await ctx.send('The shop is still under construction, stay tuned!')

@client.command()
async def me(ctx):
    """gets user profile and displays it in chat"""
    user = database_methods.get_user_from_db(ctx.message.author.id)
    if user:
        user.name = await client.fetch_user(user.userId)
        msg = f"{ctx.message.author.mention}\n{user.outputProfile()}"
    else:
        msg = "A profile was not found for you.  If you haven't use .joinGame"
    await ctx.send(msg)

@client.command()
async def crystal(ctx):
    """gets the status of the user's breeding crystal and displays it in in chat"""
    user = database_methods.get_user_from_db(ctx.message.author.id)
    if user:
        msg=f"**Last Breeding:** {user.lastBreed}\n"\
        f"Crystal Full in {user.daysUntilFull()} days"
        await ctx.send(msg)
        await ctx.send(user.BREEDINGSTONELINKS[user.breedingLevel()])

@client.command()
async def inventory(ctx):
    await ctx.send(f"Fetching Inventory {ctx.message.author.mention}")
    user = database_methods.get_user_from_db(ctx.message.author.id)
    await ctx.send(user.outputInventory())
    await ctx.send("For more information on an item, use .getItem <ID Number>")

@client.command()
async def getID(ctx):
    userId = ctx.message.author.id
    await ctx.send(f"Your unique ID is {userId}")

@client.command(require_var_positional=True)
async def getCreature(ctx,creatureId):
    requestedCreature = database_methods.get_creature_from_db(creatureId)
    if requestedCreature:
        user = await client.fetch_user(requestedCreature.owner)
        requestedCreature.ownerName = user.name
        await ctx.send(requestedCreature.outputCreature())
        await ctx.send(requestedCreature.imageLink)
    else:
        await ctx.send(f"ID Number {creatureId} not found")

@client.command()
async def joinGame(ctx):
    newUser = User(ctx.message.author.id)
    if database_methods.add_user_to_database(newUser):
        msg=f"Welcome to Chorumfur {await client.fetch_user(ctx.message.author.id)}"
    else:
        msg="Failed to add new user, perhaps you are already registered?  Try .me"
    await ctx.send(msg)

@client.command()
@is_guild_owner_or_me()
async def makeCreature(ctx,creatureName):
    userId = ctx.message.author.id
    if not ctx.message.attachments:
        msg="Attachment not detected, new Chorumfur submissions require an image."
    else:
        creatureToAdd = Creature(creatureName,userId,ctx.message.attachments[0].url)
        creatureId = database_methods.add_creature_to_db(creatureToAdd)
        msg=f"{creatureName} created with Id #{creatureId}"
    await ctx.send(msg)

@client.command()
@is_guild_owner_or_me()
async def makeItem(ctx,itemName,itemDesc,itemValue):
    if ctx.message.attachments:
        imageLink = ctx.message.attachments[0].url
    else:
        imageLink = ""
    itemToAdd = Item(itemName,itemDesc,itemValue,imageLink)
    itemId = database_methods.add_item_to_db(itemToAdd)
    if itemId:
        await ctx.send(f'{itemName} created with ID # {itemId}')
    else:
        await ctx.send(f'{itemName} cannot be created, an error occurred.')

@client.command()
@is_guild_owner_or_me()
async def getAllItems(ctx):
    await ctx.send(f"{ctx.message.author.mention}\n{database_methods.get_all_items_from_db()}")

@client.command()
@is_guild_owner_or_me()
async def addItemToInv(ctx,item_id_to_add,quantity=1):
    user_id = ctx.message.author.id
    if database_methods.add_item_to_user(user_id,item_id_to_add,quantity):
        await ctx.send("Inventory update successful.")
    else:
        await ctx.send("Inventory update failed.")

@client.command()
@is_guild_owner_or_me()
async def removeItemFromInv(ctx,item_id_to_remove,quantity=1):
    user_id = ctx.message.author.id
    if database_methods.remove_item_from_user(user_id,item_id_to_remove,quantity):
        await ctx.send("Item removed from User Inventory")
    else:
        await ctx.send("Item not found, or not successfully removed.")

@client.command()
async def getItem(ctx,item_id):
    item=database_methods.get_item_from_db(item_id)
    await ctx.send(f"{ctx.message.author.mention}\n{item.outputItem()}")
    if item.imageLink != "":
        await ctx.send(item.imageLink)
# END OF COMMANDS SECTION
f = open(os.path.abspath(os.path.join(os.path.dirname(__file__), '../token.txt')))
token = f.readline()

client.run(token)
