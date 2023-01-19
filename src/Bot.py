import os
import discord
import Database
from Creature import Creature
from User import User
from Item import Item
from discord.ext import commands
from ConstantData import Constants
discord.app_commands.CommandTree

intents = discord.Intents.default()
intents.message_content = True

game = discord.Game('with all these Chorumfurs!')

client = commands.Bot(command_prefix='.',intents=intents,activity=game)
def is_guild_owner_or_me():
    def predicate(ctx):
        return ctx.guild is not None and (ctx.guild.owner_id == ctx.author.id or ctx.author.id == 202632427535859712)
    return commands.check(predicate)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_command_error(ctx, error):
    print(f"{ctx.message.author}: {error}")
    await ctx.send(f"Command {ctx.message.content} is not recognized or you"\
        " do not have permission to perform this action.")


# BEGIN COMMANDS SECTION
@client.command()
async def shop(ctx):
    await ctx.send(f'The shop is still under construction, stay tuned!')

@client.command()
async def me(ctx):
    """Displays information about the user that entered the command."""
    user = Database.getUserFromDB(ctx.message.author.id)
    if user:
        user.name = await client.fetch_user(user.userId)
        msg = f"{ctx.message.author.mention}\n{user.outputProfile()}"
    else:
        msg = "A profile was not found for you.  If you haven't use .joinGame"
    await ctx.send(msg)

@client.command()
async def crystal(ctx):
    user = Database.getUserFromDB(ctx.message.author.id)
    if user:
        msg=f"**Last Breeding:** {user.lastBreed}\n"\
        f"Crystal Full in {user.daysUntilFull()} days"
        await ctx.send(msg)
        await ctx.send(user.BREEDINGSTONELINKS[user.breedingLevel()])

@client.command()
async def inventory(ctx):
    await ctx.send(f"Fetching Inventory {ctx.message.author.mention}")
    user = Database.getUserFromDB(ctx.message.author.id)
    await ctx.send(user.outputInventory())
    await ctx.send("For more information on an item, use .getItem <ID Number>")

@client.command()
async def getID(ctx):
    userId = ctx.message.author.id
    await ctx.send(f"Your unique ID is {userId}")

@client.command(require_var_positional=True)
async def getCreature(ctx,creatureId):
    requestedCreature = Database.getCreatureFromDB(creatureId)
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
    if Database.addUserToDB(newUser):
        msg=f"Welcome to Chorumfur {await client.fetch_user(ctx.message.author.id)}"
    else:
        msg=f"Failed to add new user, perhaps you are already registered?  Try .me"
    await ctx.send(msg)

@client.command()
async def getItem(ctx,itemId):
    item=Database.getItemFromDB(itemId)
    await ctx.send(f"{ctx.message.author.mention}\n{item.outputItem()}")
    if item.imageLink != "":
        await ctx.send(item.imageLink)

@client.command()
async def requestBreed(ctx,parent_a,parent_b):
    """Submit a breeding ticket.
    SYNTAX: .requestBreed <ID of Parent A> <ID of Parent B>"""
    author = ctx.message.author
    parent_a_output = Database.getCreatureFromDB(parent_a)
    parent_b_output = Database.getCreatureFromDB(parent_b)
    if parent_a_output and parent_b_output:
        channel = await client.fetch_channel(1061868480086941716)
        owner = await client.fetch_user(101509826588205056)
        msg = f"""{owner.mention}
        User {author} has requested the following breeding:
        **Parent A:** {parent_a_output.name} ({parent_a})
        **Parent B:** {parent_b_output.name} ({parent_b})"""
        await channel.send(msg)
        await ctx.send("**Justin**, God of all things sex, has heard your " +
        f"request and taken **{parent_a_output.name}** and **{parent_b_output.name}** to his bedchamber.")
    else:
        await ctx.send("Parent ID not found in database.")

@client.command()
@is_guild_owner_or_me()
async def makeCreature(ctx,creatureName):
    """Creates a new creature (Admin Restricted Command).  Requires an image attachment.
    SYNTAX: .makeCreature <creature name>"""
    userId = ctx.message.author.id
    if not ctx.message.attachments:
        msg="Attachment not detected, new Chorumfur submissions require an image."
    else:
        creatureToAdd = Creature(creatureName,userId,ctx.message.attachments[0].url)
        creatureId = Database.addCreatureToDB(creatureToAdd)
        msg=f"{creatureName} created with Id #{creatureId}"
    await ctx.send(msg)
@client.command()
@is_guild_owner_or_me()
async def makeRandomCreature(ctx,creature_name):
    """Creates a new creature with random traits"""
    user_id = ctx.message.author.id
    new_creature = Creature(creature_name,user_id,"No Image Available")
    new_creature.randomize_creature()
    msg = f"""Main Horn: {Constants.MAIN_HORN[new_creature.traits['MAIN_HORN']]}
                 Cheek Horn: {Constants.CHEEK_HORN[new_creature.traits['CHEEK_HORN']]}
                 Face Horn: {Constants.FACE_HORN[new_creature.traits['FACE_HORN']]}
                 Tail: {Constants.TAIL[new_creature.traits['TAIL']]}
                 Tail Tip: {Constants.TAIL_TIP[new_creature.traits['TAIL_TIP']]}
                 Fluff: {Constants.FLUFF[new_creature.traits['FLUFF']]}
                 """
    if new_creature.traits['MUTATION']:
        msg += f"""Mutation: {Constants.MUTATION[new_creature.traits['MUTATION']]}"""
    ctx.send(msg)

@client.command()
@is_guild_owner_or_me()
async def makeItem(ctx,itemName,itemDesc,itemValue):
    """Creates a new item and adds it to the global items database.
    SYNTAX: .makeItem <Item Name> <Item Description> <Item Value>"""
    if ctx.message.attachments:
        imageLink = ctx.message.attachments[0].url
    else:
        imageLink = ""
    itemToAdd = Item(itemName,itemDesc,itemValue,imageLink)
    itemId = Database.addItemToDB(itemToAdd)
    if itemId:
        await ctx.send(f'{itemName} created with ID # {itemId}')
    else:
        await ctx.send(f'{itemName} cannot be created, an error occurred.')

@client.command()
@is_guild_owner_or_me()
async def getAllItems(ctx):
    await ctx.send(f"{ctx.message.author.mention}\n{Database.getAllItemsInDB()}")

@client.command()
@is_guild_owner_or_me()
async def addItemToInv(ctx,itemIDToAdd):
    user = Database.getUserFromDB(ctx.message.author.id)
    if Database.addToUserInventory(user.userId,itemIDToAdd):
        await ctx.send(f"Item {Database.getItemFromDB(itemIDToAdd).name} added to your user.")
    else:
        await ctx.send(f"Adding Item {Database.getItemFromDB(itemIDToAdd).name}failed.")

@client.command()
@is_guild_owner_or_me()
async def removeItemFromInv(ctx,itemIDToRemove):
    user = Database.getUserFromDB(ctx.message.author.id)
    if Database.removeFromUserInventory(user.userId,itemIDToRemove):
        await ctx.send("Item removed from User Inventory")
    else:
        await ctx.send(f"Item not found, or not successfully removed.")

# END OF COMMANDS SECTION
f = open(os.path.abspath(os.path.join(os.path.dirname(__file__), '../token.txt')))
token = f.readline()

client.run(token)