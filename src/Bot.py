import os
import discord
import logging
from discord.ext import commands
from Creature import Creature
from User import User
from Item import Item
from Breeding import Breeding
from Ticket import Ticket
from ConstantData import Constants
import database_methods

#discord_py_logfile_location = os.path.abspath(os.path.join(os.path.dirname(__file__), '../discord.log'))
app_logfile_location = os.path.abspath(os.path.join(os.path.dirname(__file__), '../chorumfur-bot.log'))
logging.basicConfig(filename=app_logfile_location,format='%(asctime)s %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(20)
#handler = logging.FileHandler(filename=discord_py_logfile_location, encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

game = discord.Game('with all these Chorumfurs!')

client = commands.Bot(command_prefix='.',intents=intents,activity=game)

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
        user.name = client.get_user(ctx.message.author.id)
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

@client.command(aliases=['gc','getcreature'],require_var_positional=True)
async def getCreature(ctx,creatureId):
    requestedCreature = database_methods.get_creature_from_db(creatureId)
    if requestedCreature:
        user = client.get_user(requestedCreature.owner)
        requestedCreature.ownerName = user.name
        await ctx.send(requestedCreature.outputCreature())
        await ctx.send(requestedCreature.imageLink)
    else:
        await ctx.send(f"ID Number {creatureId} not found")

@client.command(aliases=['join'])
async def joinGame(ctx):
    newUser = User(ctx.message.author.id)
    if database_methods.add_user_to_database(newUser):
        msg=f"Welcome to Chorumfur {client.get_user(ctx.message.author.id)}"
    else:
        msg="Failed to add new user, perhaps you are already registered?  Try .me"
    await ctx.send(msg)

@client.command(require_var_positional=True)
@is_guild_owner_or_me()
async def makeCreature(ctx,creatureName):
    userId = ctx.message.author.id
    if not ctx.message.attachments:
        msg="Attachment not detected, new Chorumfur submissions require an image."
    else:
        creatureToAdd = Creature(name = creatureName,owner = userId,imageLink = ctx.message.attachments[0].url)
        creatureId = database_methods.add_creature_to_db(creatureToAdd)
        msg=f"{creatureName} created with Id #{creatureId}"
    await ctx.send(msg)

@client.command()
@is_guild_owner_or_me()
async def makeRandomCreature(ctx,creatureName):
    userId = ctx.message.author.id
    creature_to_add = Creature(creatureName,userId)
    creature_to_add.randomize_creature()
    creature_id = database_methods.add_creature_to_db(creature_to_add)
    if creature_id:
        creature_to_add.creatureId=creature_id
        await ctx.send(f"{creatureName} added to database with ID #{creature_id}")
        await ctx.send(creature_to_add.outputCreature())
    else:
        await ctx.send(f"An error occurred adding {creatureName} to the database")

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
    output = "**Item ID | Item Name - Item Value**\n```"
    for item in database_methods.get_all_items_from_db():
        output+= f"{item[0]} | {item[1]} - {item[2]}\n"
    output+= "```**For more information run `.getItem <Item ID>`**"
    await ctx.send(output)

@client.command()
@is_guild_owner_or_me()
async def addItemToInv(ctx,item_id_to_add,user_id = None,quantity=1):
    """adds an item to a given users inventory with a given quantity.
    If no user ID is specified, items will be given to the user who invoked the command.
    If a quantity is not specified, it will add 1."""
    if user_id is None:
        user_id = ctx.message.author.id
    if database_methods.add_item_to_user(user_id,item_id_to_add,quantity):
        await ctx.send("Inventory update successful.")
    else:
        await ctx.send("Inventory update failed.")

@client.command()
@is_guild_owner_or_me()
async def removeItemFromInv(ctx,item_id_to_remove,user_id = None,quantity=1):
    if user_id is None:
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

@client.command()
async def breed(ctx,creature_a_id,creature_b_id):
    """Submit a breeding request in format .breed <creature_a> <creature_b>"""
    requesting_user = database_methods.get_user_from_db(ctx.message.author.id)
    creature_a=database_methods.get_creature_from_db(creature_a_id)
    creature_b=database_methods.get_creature_from_db(creature_b_id)
    parents_of_a=database_methods.get_parents_from_db(creature_a)
    parents_of_b=database_methods.get_parents_from_db(creature_b)
    breed_request = Ticket(ticket_name=f"{creature_a.name} x {creature_b.name}",
                           ticket_requestor=requesting_user,
                           creature_a=creature_a,
                           creature_b=creature_b,
                           parents_of_a=parents_of_a,
                           parents_of_b=parents_of_b)
    if breed_request.requestor_can_breed():
        if breed_request.requestor_owns_both():
            # When requestor owns both, breeding processing can go ahead without pause.
            breed_request.update_ticket_status(3)
            requesting_user.update_last_breed()
            database_methods.update_user_last_breed(requesting_user)
            breed_request.perform_breeding()
            breed_request = add_pups_to_database(breed_request)
            breed_request.id = database_methods.add_ticket_to_db(breed_request)
            await send_ticket_to_channel(breed_request)
        else:
            # Otherwise breeding is put on hold until the receiving user uses .accept
            breed_request.update_ticket_status(2)
            breed_request.id = database_methods.add_ticket_to_db(breed_request)
            pending_breedings = client.get_channel(1067121489444339844)
            other_user = client.get_user(breed_request.other_user())
            await pending_breedings.send(f"{other_user.mention}: Please use .accept "\
                f"{breed_request.id} to confirm the following breeding, or "\
                f".decline {breed_request.id} to reject it.  Unanswered tickets"\
                " will expire after 30 days.\n"\
                f"{breed_request.output_ticket()}")
        await ctx.send(f"Ticket #{breed_request.id} has been submitted for "\
                       f"breeding with a status of {breed_request.status}")
    else:
        await ctx.send("Breeding request was not able to be submitted at this time."\
                " Please confirm you own at least one of the creatures submitted "\
                "and that your breeding crystal is fully charged.")

@client.command(aliases=['accept'])
async def acceptBreeding(ctx,ticket_id):
    ticket = database_methods.get_ticket_from_db(ticket_id)
    if ticket.other_user() != ctx.message.author.id:
        msg = "You do not have permission to modify this ticket."
    elif ticket.status != Constants.TICKET_STATUS[2]:
        msg = f"This ticket is in {ticket.status} and cannot be modified."
    else:
        #Do all the breeding stuff put on hold
        ticket.update_ticket_status(3)
        ticket.requestor.update_last_breed()
        database_methods.update_user_last_breed(ticket.requestor)
        ticket.perform_breeding()
        ticket = add_pups_to_database(ticket)
        database_methods.update_ticket_in_db(ticket)
        await send_ticket_to_channel(ticket)
        msg = f"Ticket {ticket.id} has been accepted.  Status is now {ticket.status}"
    await ctx.send(msg)

@client.command(aliases=['decline'])
async def declineBreeding(ctx,ticket_id):
    ticket = database_methods.get_ticket_from_db(ticket_id)
    if ticket.other_user() != ctx.message.author.id:
        msg = "You do not have permission to modify this ticket."
    elif ticket.status != Constants.TICKET_STATUS[2]:
        msg = f"This ticket is in {ticket.status} and cannot be modified."
    else:
        ticket.update_ticket_status(6)
        database_methods.update_ticket_in_db(ticket)
        msg = f"Ticket {ticket.id} has been rejected.  Status is now {ticket.status}"
    await ctx.send(msg)

@client.command(aliases=['gt'])
async def getTicket(ctx,ticket_id):
    """Retreives a ticket from the database by ID number."""
    returned_ticket = database_methods.get_ticket_from_db(ticket_id)
    await ctx.send(returned_ticket.output_ticket())

@client.command(aliases=['mt'])
async def myTickets(ctx):
    """Retreives data on all tickets user currently has and returns it as a formatted output"""
    user_id = ctx.message.author.id
    returned_tickets = database_methods.get_my_tickets_from_db(user_id)
    output="**ID# | Ticket Name - Ticket Status**\n```"
    for ticket in returned_tickets:
        output+=f"{ticket[0]} | {ticket[1]} - {ticket[2]}\n"
    output+="```**For more information run `.getTicket <ticket ID>`**"
    await ctx.send(output)


@is_guild_owner_or_me()
@client.command(aliases=['gdt'])
async def getDetailedTicket(ctx,ticket_id):
    """Retrieves a ticket from the database and outputs a detailed breeding ticket"""
    returned_ticket = database_methods.get_ticket_from_db(ticket_id)
    await ctx.send(returned_ticket.output_detailed_ticket())

@is_guild_owner_or_me()
@client.command(aliases=['at'])
async def advanceTicket(ctx,ticket_id):
    """Advances the status of a given ticket one step"""
    ticket = database_methods.get_ticket_from_db(ticket_id)
    status_code = Constants.TICKET_STATUS.index(ticket.status)
    if status_code == 2:
        await ctx.send("Ticket is currently awaiting confirmation from a user.  It cannot be updated.")
    elif status_code == 5:
        await ctx.send("Ticket already has a status of Complete, cannot advance.")
    else:
        status_code += 1
        ticket.status = Constants.TICKET_STATUS[status_code]
        database_methods.update_ticket_status()

@client.command()
async def cancelTicket(ctx,ticket_id):
    """Cancels an in progress breeding ticket"""
    ticket = database_methods.get_ticket_from_db(ticket_id)
    if ctx.message.author.id != ticket.requestor.userId:
        msg = "You do not have permission to modify this ticket."
    elif ticket.status == Constants.TICKET_STATUS[5]:
        msg = "You cannot cancel a completed ticket."
    else:
        if database_methods.delete_ticket(ticket_id):
            msg = "Your ticket has been successfully removed from the database."
            tickets_channel = client.get_channel(1061868480086941716)
            artist = client.get_user(101509826588205056)
            await tickets_channel.send(f"{artist.mention} **User has requested cancellation"\
                                f"of ticket #{ticket.id}**")
        else:
            msg="An error occurred deleting your ticket from the database."
    await ctx.send(msg)

@client.command()
@is_guild_owner_or_me()
async def showTickets(ctx,type_to_show='open'):
    """Shows a summary view of all open tickets based on a parameter.  Accepts 'open'
    to show all open tickets or 'pending' to show tickets in a Breeding Pending state."""
    type_to_show = type_to_show.lower()
    returned_tickets = database_methods.get_requested_tickets_from_db(type_to_show)
    output="**ID# | Ticket Name - Ticket Status**\n```"
    for ticket in returned_tickets:
        output+=f"{ticket[0]} | {ticket[1]} - {ticket[2]}\n"
    output+="```**For more information run `.getTicket <ticket ID>`**"
    await ctx.send(output)

@client.command(aliases=['ml','lair'])
async def myLair(ctx):
    user_id = ctx.message.author.id
    returned_creatures = database_methods.get_my_creatures_from_db(user_id)
    output="**ID# | Creature Name**\n```"
    for creature in returned_creatures:
        output+=f"{creature[0]} | {creature[1]}\n"
    output+="```**For more information run `.getCreature <Creature ID>`**"
    await ctx.send(output)

@client.command()
@is_guild_owner_or_me()
async def adminBreed(ctx,creature_a_id,creature_b_id):
    """ADMIN: Submit a breeding request in format .breed <creature_a> <creature_b>
       DOES NOT USE BREEDING CRYSTAL"""
    requesting_user = database_methods.get_user_from_db(ctx.message.author.id)
    creature_a=database_methods.get_creature_from_db(creature_a_id)
    creature_b=database_methods.get_creature_from_db(creature_b_id)
    parents_of_a = database_methods.get_parents_from_db(creature_a)
    parents_of_b = database_methods.get_parents_from_db(creature_b)
    breed_request = Breeding(creature_a,creature_b,requesting_user.userId,parents_of_a,parents_of_b)
    pups = breed_request.breed()
    pup_ids=[]
    for pup in pups:
        pup_ids.append(database_methods.add_creature_to_db(pup))
    await ctx.send(f"Breeding Complete, ID #s {pup_ids} added to DB")

# END OF COMMANDS SECTION
f = open(os.path.abspath(os.path.join(os.path.dirname(__file__), '../token.txt')))
token = f.readline()

client.run(token)
