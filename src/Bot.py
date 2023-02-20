"""Manages user interaction using discord.py"""
import os
import logging
from environment import EnvironmentVars
from ConstantData import Constants
import discord
from discord.ext import commands

app_logfile_location = os.path.abspath(os.path.join(os.path.dirname(__file__), '../chorumfur-bot.log'))
logging.basicConfig(filename=app_logfile_location,format='%(asctime)s %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(20)
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

cogs = ['cogs.cog_admin',
        'cogs.cog_breeding',
        'cogs.cog_creatures',
        'cogs.cog_inventory',
        'cogs.cog_tickets',
        'cogs.cog_users']

game = discord.Game('with all these Chorumfurs!')
client = commands.Bot(command_prefix=EnvironmentVars.bot_invocation_var,intents=intents,activity=game)

@client.event
async def on_ready():
    """Called when discord bot is ready to use"""
    logging.info('We have logged in as %s',client.user)

@client.event
async def on_command_error(ctx, error):
    """Triggers when a command is not processed successfully"""
    logger.info("%s:%s Command failed",ctx.message.author,ctx.message.content)
    logger.warning(error)
    await ctx.send(f"Command {ctx.message.content} is not recognized or you"\
       " do not have permission to perform this action.")

@client.event
async def on_member_join(member):
    """Triggers when a member joins and sends them a welcome message"""
    landing_zone = client.get_channel(1067121892223369278)
    rules_channel = client.get_channel(1067133274796871803)
    await landing_zone.send(f"Welcome to Chorumfur, {member.mention}!  To get started, check out the {rules_channel.mention} "\
        "and then use `.joinGame` to start playing!")

@client.event
async def setup_hook():
    for cog in cogs:
        await client.load_extension(cog)

@client.command()
async def about(ctx):
    """Displays data about chorumfur-bot"""
    msg=f"""**Chorumfur-Bot {Constants.VERSION}**
    Chorumfur-bot is programmed entirely in Python using the Discord.py library
    by Justin Gordon ({client.get_user(202632427535859712)})
    Code and documentation available at: https://github.com/A554551N/chorumfur-bot

    Chorumfurs are small ferret-like dragons originally created by Quinn#0610, then apprehendedand run off with by Lysa (Zombpossum#5577).

    While the species has been around since 2019, this community has only been operating sinc late 2022.  There's a whole rich culture behind these fuzzbutts that we're excited to share and release to you all as we continue to grow and expand!

    Chorumfurs are a closed species, the only way to get one is to be part of our community.
    """
    await ctx.send(msg)

# Gets bot token and stores it in the token variable
f = open(os.path.abspath(os.path.join(os.path.dirname(__file__), '../token.txt')))
token = f.readline()

client.run(token)
