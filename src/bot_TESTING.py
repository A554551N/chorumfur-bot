"""Manages user interaction using discord.py"""
import os
import logging
import discord
from discord.ext import commands
from Creature import Creature
from User import User
from Item import Item
from Ticket import Ticket
from ConstantData import Constants
import database_methods

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

client = commands.Bot(command_prefix='!',intents=intents,activity=game)

def is_guild_owner_or_me():
    """Checks to see if the author of a message is guild_owner or bot creator"""
    def predicate(ctx):
        return ctx.guild is not None and (ctx.guild.owner_id == ctx.author.id or ctx.author.id == 202632427535859712)
    return commands.check(predicate)

async def send_ticket_to_channel(ticket):
    """Sends a message to the tickets channel and mentions artist"""
    artist = client.get_user(101509826588205056)
    ticket_channel = client.get_channel(1061868480086941716)
    await ticket_channel.send(artist.mention)
    await ticket_channel.send(ticket.output_detailed_ticket())

def add_pups_to_database(ticket):
    """Iterates over the pups parameter of a ticket object and adds them to database."""
    for pup in ticket.pups:
        pup.creatureId = database_methods.add_creature_to_db(pup)
    return ticket

def strip_mention_format(mention):
    """removes leading <@ and trailing > from user IDs passed as mentions"""
    return mention[2:-1]

def enact_breeding(ticket):
    """Performs the core logic of breeding based on a supplied Ticket object.
    Returns the updated Ticket object"""
    ticket.update_ticket_status(3)
    ticket.requestor.update_last_breed()
    database_methods.update_user_last_breed(ticket.requestor)
    ticket.perform_breeding()
    ticket = add_pups_to_database(ticket)
    return ticket

async def pend_breeding(ctx,ticket):
    """Creates a Ticket in a Pending state and submits the information to the
     pending_breedings channel.  Returns the modified Ticket."""
    ticket.update_ticket_status(2)
    ticket.id = database_methods.add_ticket_to_db(ticket)
    pending_breedings = client.get_channel(1067121489444339844)
    other_user = client.get_user(ticket.other_user())
    await pending_breedings.send(
        f"{other_user.mention}: Please use .accept "\
        f"{ticket.id} to confirm the following breeding, or "\
        f".decline {ticket.id} to reject it.  Unanswered tickets"\
        " will expire after 30 days.\n"\
        f"{ticket.output_ticket()}")
    await ctx.send(f"Ticket #{ticket.id} has been submitted for "\
                   f"breeding with a status of {ticket.status}")

def create_breeding_ticket(requesting_user_id,creature_a_id,creature_b_id):
    """Takes in a user ID and two creature IDs and returns a breeding Ticket"""
    requesting_user = database_methods.get_user_from_db(requesting_user_id)
    creature_a=database_methods.get_creature_from_db(creature_a_id)
    creature_b=database_methods.get_creature_from_db(creature_b_id)
    parents_of_a=database_methods.get_parents_from_db(creature_a)
    parents_of_b=database_methods.get_parents_from_db(creature_b)
    return Ticket(ticket_name=f"{creature_a.name} x {creature_b.name}",
                           ticket_requestor=requesting_user,
                           creature_a=creature_a,
                           creature_b=creature_b,
                           parents_of_a=parents_of_a,
                           parents_of_b=parents_of_b)

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

# BEGIN COMMANDS SECTION
# MARK FOR REMOVAL
@client.command()
async def shop(ctx):
    """Command triggers the shop interface"""
    await ctx.send('The shop is still under construction, stay tuned!')

# END OF COMMANDS SECTION

# Gets bot token and stores it in the token variable
f = open(os.path.abspath(os.path.join(os.path.dirname(__file__), '../token.txt')))
token = f.readline()

client.run(token)
