import os
import discord
import Database
import Creature
from discord.ext import commands
discord.app_commands.CommandTree

intents = discord.Intents.default()
intents.message_content = True

game = discord.Game('with all these Chorumfurs!')
client = commands.Bot(command_prefix='.',intents=intents,activity=game)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

# BEGIN COMMANDS SECTION
@client.command()
async def hello(ctx):
    await ctx.send(f'Hello {ctx.author}')

@client.command()
async def shop(ctx):
    await ctx.send(f'The shop is still under construction, stay tuned!')

@client.command()
async def me(ctx):
    await ctx.send('Hi {}, profiles are a work in progress.\nStand by!'.format(ctx.message.author.mention))

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
    await ctx.send(requestedCreature.outputCreature())



# END OF COMMANDS SECTION
f = open(os.path.abspath(os.path.join(os.path.dirname(__file__), '../token.txt')))
token = f.readline()

client.run(token)