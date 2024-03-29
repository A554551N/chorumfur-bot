from datetime import datetime
from discord.ext import commands
from Creature import Creature
from Item import Item
from ConstantData import Constants
import database_methods
import support_functions

def is_guild_owner_or_bot_admin():
    """Checks to see if the author of a message is guild_owner or bot creator"""
    def predicate(ctx):
        # removing ctx.guild is not None here would allow DMing admin commands to bot
        return ctx.author.id in (101509826588205056,202632427535859712)
    return commands.check(predicate)

class AdminCog(commands.GroupCog, name='Admin Tools', group_name='admin'):
    """Cog to group commands accessible only to admins"""

    def __init__(self, bot):
        self.client = bot

    @commands.command(aliases=['mc'])
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

    @commands.command(aliases=['mrc'])
    @is_guild_owner_or_bot_admin()
    async def makeRandomCreature(self,ctx,quantity=1):
        """Takes in an optional quantity parameter and stores that many creatures in the database
        with randomized traits.  Outputs the creature to the interface after completion.
        Random Creatures are always owned by account 0 (the system)"""
        creatures_to_add = []
        for count in range(1,quantity+1):
            creature_to_add = Creature(f"Random {count}",0)
            creature_to_add.randomize_creature()
            creatures_to_add.append(creature_to_add)
        returned_ids = database_methods.add_multiple_creatures_to_db(creatures_to_add)
        output = "The following creatures have been added to the database: "
        for returned_id in returned_ids:
            output+= f"{returned_id[0]} "
        await ctx.send(output)

    @commands.command(aliases=['mi'])
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

    @commands.command(aliases=['gai'])
    @is_guild_owner_or_bot_admin()
    async def getAllItems(self,ctx):
        """Retrieves all items defined in the items database and displays them as a list."""
        returned_items = database_methods.get_all_items_from_db() or None
        if returned_items:
            msg_list = support_functions.format_output("{} - {} - {}\n",
                                                       ("ID#","Item Name","Value"),
                                                        returned_items
                                                      )
        for msg in msg_list:
            await ctx.send(msg if returned_items else "No Items Found")
        await ctx.send("**For more information run `.getItem <Item ID>`**")

    @commands.command(aliases=['addInv'])
    @is_guild_owner_or_bot_admin()
    async def addItemToInv(self,ctx,item_id_to_add,user_id = None,quantity=1):
        """adds an item to a given users inventory with a given quantity.
        If no user ID is specified, items will be given to the user who invoked the command.
        If a quantity is not specified, it will add 1.
        
        Parameters
        ----------
        item_id : int
            The item_id to add
        user_id : string
            user_id (as an @ mention)
        quantity : int
            number of items to add
        """
        
        if user_id is None:
            user_id = ctx.message.author.id
        else:
            user_id = support_functions.strip_mention_format(user_id)
        if database_methods.add_item_to_user(user_id,item_id_to_add,quantity):
            await ctx.send("Inventory update successful.")
        else:
            await ctx.send("Inventory update failed.")

    @commands.command(aliases=['remInv'])
    @is_guild_owner_or_bot_admin()
    async def removeItemFromInv(self,ctx,item_id_to_remove,user_id = None,quantity=1):
        """ADMIN COMMAND: Removes a given quantity of an item from a given user's inventory.
        If no user is specified, removes an item from your own inventory.
        If no quantity is specified, removes 1."""
        if user_id is None:
            user_id = ctx.message.author.id
        else:
            user_id = support_functions.strip_mention_format(user_id)
        if database_methods.remove_item_from_user(user_id,item_id_to_remove,quantity):
            await ctx.send("Item removed from User Inventory")
        else:
            await ctx.send("Item not found, or not successfully removed.")

    @commands.command(aliases=['gdt'])
    @is_guild_owner_or_bot_admin()
    async def getDetailedTicket(self,ctx,ticket_id):
        """Retrieves a ticket from the database and outputs a detailed breeding ticket"""
        returned_ticket = database_methods.get_ticket_from_db(ticket_id)
        pups = database_methods.get_multiple_creatures_from_db(returned_ticket.pups)
        parents = database_methods.get_parents_from_db(pups[0])
        for pup in pups:
            pup.parents = parents
        await ctx.send(returned_ticket.output_detailed_ticket(pups))

    @is_guild_owner_or_bot_admin()
    @commands.command(aliases=['at'])
    async def advanceTicket(self,ctx,ticket_id):
        """Advances the status of a given ticket one step"""
        ticket = database_methods.get_ticket_from_db(ticket_id)
        status_code = Constants.TICKET_STATUS.index(ticket.status)
        if status_code == 2:
            await ctx.send("Ticket is currently awaiting confirmation from a user.  It cannot be updated.")
        elif status_code == 6:
            await ctx.send("Ticket already has a status of Complete, cannot advance.")
        else:
            status_code += 1
            if ticket.type == 'modification' and ticket.status == Constants.TICKET_STATUS[4]:
                status_code = 6
            ticket.status = Constants.TICKET_STATUS[status_code]
            database_methods.update_ticket_status(ticket)
            await ctx.send(f"Ticket {ticket.id} updated to status {ticket.status}")

    @commands.command(aliases=['st'])
    @is_guild_owner_or_bot_admin()
    async def showTickets(self,ctx,type_to_show='open'):
        """Shows a summary view of all open tickets based on a parameter.  Accepts 'open'
        to show all open tickets or 'pending' to show tickets in a Breeding Pending state.
        'ready' displays all creatures in a Ready to Birth State"""
        type_to_show = type_to_show.lower()
        returned_tickets = database_methods.get_requested_tickets_from_db(type_to_show) or None
        if returned_tickets:
            msg_list=support_functions.format_output("{} - {} - {}\n",
                                            ("ID#","Ticket Name","Ticket Status"),
                                            returned_tickets)
            for msg in msg_list:
                await ctx.send(msg)
            await ctx.send("**For more information run `.getTicket <ticket ID>`**")
        else:
            await ctx.send("No Tickets Found")

    @commands.command(aliases=['imageUpdate','ui'])
    @is_guild_owner_or_bot_admin()
    async def updateImage(self,ctx,creature_id,*args):
        """ADMIN COMMAND: Updates a chorumfur with a given id's displayed image.
        .updateImage <creature_id> newborn|<newborn url> pup|<pup url> adult|<adult url>.
        All keywords are optional but at least one must be specified."""
        creature_to_update = database_methods.get_creature_from_db(creature_id)
        # This code is necessary to parse arguments from *args.  Can be refactored
        # if support for kwargs is found.
        for argument in args:
            split_argument = argument.split("|")
            if split_argument[0].lower() == 'adult':
                creature_to_update.imageLink = split_argument[1]
            if split_argument[0].lower() == 'newborn':
                creature_to_update.imageLink_nb = split_argument[1]
            if split_argument[0].lower() == 'pup':
                creature_to_update.imageLink_pup = split_argument[1]
        if database_methods.update_creature(creature_to_update):
            await ctx.send("Chorumfur has been updated successfully.")
        else:
            await ctx.send("The chorumfur could not be updated.")

    @commands.command(aliases=['adm'])
    @is_guild_owner_or_bot_admin()
    async def adminMate(self,ctx,creature_a_id,creature_b_id,new_owner=None):
        """ADMIN: Submit a mating request in format .mate <creature_a> <creature_b> <new owner>
        DOES NOT USE BREEDING CRYSTAL"""
        if new_owner is None:
            new_owner = ctx.message.author.id
        else:
            new_owner = support_functions.strip_mention_format(new_owner)
        ticket = support_functions.create_breeding_ticket(requesting_user_id=new_owner,
                                       creature_a_id=creature_a_id,
                                       creature_b_id=creature_b_id,
                                       item_to_use=None)
        support_functions.enact_breeding(ticket,is_admin=True)
        ticket.id = database_methods.add_ticket_to_db(ticket)
        await support_functions.send_ticket_to_channel(self.client,ticket)
        await ctx.send("Breeding has been successfully submitted.  "\
                       f"Ticket # is {ticket.id}")

    @commands.command(aliases=['agc'])
    @is_guild_owner_or_bot_admin()
    async def adminGiveCreature(self,ctx,creature_id,new_owner):
        """Gives creatures with a given ID to a mentioned new owner.
        Does not check current ownership"""
        creature_to_give = database_methods.get_creature_from_db(creature_id)
        creature_to_give.owner = support_functions.strip_mention_format(new_owner)
        if database_methods.update_creature(creature_to_give):
            await ctx.send("Creature has been given to requested user.")
        else:
            await ctx.send("An error has occurred, your creature has not been transferred.")

    @commands.command(aliases=['birth'])
    @is_guild_owner_or_bot_admin()
    async def giveBirth(self,ctx,ticket_id):
        """Takes in a Ticket ID and updates the createDate of pups on the ticket."""
        ticket = database_methods.get_ticket_from_db(ticket_id)
        for pup_id in ticket.pups:
            # leaving this here through next breeding in case any pups are still on old model
            pup = database_methods.get_creature_from_db(pup_id)
            pup.createDate = datetime.today()
            pup.owner = ticket.requestor.userId
            database_methods.update_creature(pup)
            #support_functions.add_pups_to_database(ticket)
        await ctx.send(f"Litter for ticket #{ticket.id} birthed and "\
                       f" delivered to <@{ticket.requestor.userId}>")

    @commands.command()
    @is_guild_owner_or_bot_admin()
    async def movePupsToDB(self,ctx):
        for ticket_id in (18,19,20,21,22):
            ticket = database_methods.get_ticket_from_db(ticket_id)
            pup_list = database_methods.add_multiple_creatures_to_db(ticket.pups)
            ticket.pups = pup_list
            await ctx.send(f"{ticket.id} - {ticket.pups}")
            database_methods.update_ticket_in_db(ticket)

    @commands.command()
    @is_guild_owner_or_bot_admin()
    async def birthAll(self,ctx):
        """automatically births ALL creatures in 'Ready to Birth' status."""
        tickets = database_methods.get_tickets_from_db_by_status(5) or None
        if tickets:
            completed_tickets = []
            completed_pups = 0
            for ticket in tickets:
                print(ticket.pups)
                list_of_pups = database_methods.get_multiple_creatures_from_db(ticket.pups)
                for pup in list_of_pups:
                    pup.createDate = datetime.today()
                    pup.owner = ticket.requestor.userId
                    print(pup.name)
                    completed_pups += 1
                    database_methods.update_creature(pup)
                    print('update successful')
                completed_tickets.append(ticket.id)
                ticket.update_ticket_status(6)
                database_methods.update_ticket_status(ticket)
            await ctx.send(f"Tickets {completed_tickets} have been birthed.\nA total of {completed_pups} were born.")
        else:
            await ctx.send("No tickets appear to be ready for breeding or an error has occurred.")

    @commands.command()
    @is_guild_owner_or_bot_admin()
    async def resetCrystal(self,ctx,user_to_reset=None):
        """Resets a given user's mating crystal.  If no user is specified, resets own crystal.
        
        Parameters
        ---------
        user_to_reset: string
            @ mentioned user to reset
        """

        if not user_to_reset:
            user_to_reset = ctx.message.author.id
        else:
            user_to_reset = support_functions.strip_mention_format(user_to_reset)
        user = database_methods.get_user_from_db(user_to_reset) or None
        try:
            user.lastBreed = None
            database_methods.update_user_last_breed(user)
            await ctx.send('User crystal updated.')
        except AttributeError:
            await ctx.send('An error occurred with your request, most likely the user'\
                           'targeted was not found.')
        

    @commands.command()
    @is_guild_owner_or_bot_admin()
    async def updateWallet(self,ctx,user_to_change,amount):
        """Adds or removes the requested amount from a user's wallet (expressed as a positive or negative number)
        Parameters
        ----------
        user_to_change: str
            an @mentioned user
        amount: int
            a positive (to add) or negative (to remove) amount of currency"""

        user_id = support_functions.strip_mention_format(user_to_change)
        database_methods.update_currency_in_wallet(user_id,amount)
        await ctx.send("User wallet updated.")

async def setup(bot):
    await bot.add_cog(AdminCog(bot))
