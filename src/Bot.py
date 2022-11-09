import os
import discord
import Database
import Creature
import User
from discord.ext import commands
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

"""
@client.event
async def on_command_error(ctx, error):
    await ctx.send(f"Command {ctx.message.content} is not recognized or you"\
        " do not have permission to perform this action.")
"""
# BEGIN COMMANDS SECTION
@client.command()
async def shop(ctx):
    await ctx.send(f'The shop is still under construction, stay tuned!')

@client.command()
async def me(ctx):
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
    await ctx.send(f"Oh no, you forgot your bag!  Don't worry, we'll find it.")

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
    newUser = User.User(ctx.message.author.id)
    if Database.addUserToDB(newUser):
        msg=f"Welcome to Chorumfur {await client.fetch_user(ctx.message.author.id)}"
    else:
        msg=f"Failed to add new user, perhaps you are already registered?  Try .me"
    await ctx.send(msg)

@client.command()
@is_guild_owner_or_me()
async def makeCreature(ctx,creatureName):
    userId = ctx.message.author.id
    if not ctx.message.attachments:
        msg="Attachment not detected, new Chorumfur submissions require an image."
    else:
        creatureToAdd = Creature.Creature(creatureName,userId,ctx.message.attachments[0].url)
        creatureId = Database.addCreatureToDB(creatureToAdd)
        msg=f"{creatureName} created with Id #{creatureId}"
    await ctx.send(msg)

# END OF COMMANDS SECTION
f = open(os.path.abspath(os.path.join(os.path.dirname(__file__), '../token.txt')))
token = f.readline()

client.run(token)