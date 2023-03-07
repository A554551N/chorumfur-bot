from discord.ext import commands
import database_methods
import support_functions

class CreaturesCog(commands.GroupCog, name='Chorumfur Management',group_name='chorumfurs'):
    """Cog to group commands related to managing creatures"""
    def __init__(self,bot):
        self.client = bot

    @commands.command(aliases=['gc','getcreature'],require_var_positional=True)
    async def getCreature(self,ctx,creatureId):
        """Takes in a creature ID and sends a formatted output of the creature to discord"""
        requested_creature = database_methods.get_creature_from_db(creatureId) or None
        if requested_creature:
            creature_parents = database_methods.get_parents_from_db(requested_creature)
            print(creature_parents)
            if creature_parents:
                requested_creature.parents = creature_parents
            if requested_creature.owner not in (0,1):
                user = self.client.get_user(requested_creature.owner)
                requested_creature.ownerName = user.name
            returned_values = requested_creature.outputCreature()
            await ctx.send(returned_values[0])
            await ctx.send(returned_values[1])
        else:
            await ctx.send(f"ID Number {creatureId} not found")

    @commands.command(aliases=['rename'])
    async def renameCreature(self,ctx,creature_id,new_name):
        """Renames a creature with a given creature ID"""
        requested_creature = database_methods.get_creature_from_db(creature_id)
        if ctx.message.author.id != requested_creature.owner:
            await ctx.send("Only a chorumfur's owner can change its' name.")
        else:
            requested_creature.name = new_name
            if database_methods.update_creature(requested_creature):
                await ctx.send("Chorumfur data successfully updated!")
            else:
                await ctx.send("Your chorumfur could not be renamed.")

    @commands.command()
    async def giveCreature(self,ctx,creature_id,new_owner):
        """Gives creatures with a given ID to a mentioned new owner."""
        creature_to_give = database_methods.get_creature_from_db(creature_id)
        if creature_to_give.owner != ctx.message.author.id:
            await ctx.send("You may only give away chorumfurs that you own.")
        else:
            creature_to_give.owner = support_functions.strip_mention_format(new_owner)
        if database_methods.update_creature(creature_to_give):
            await ctx.send("Creature has been given to requested user.")
        else:
            await ctx.send("An error has occurred, your creature has not been transferred.")

    @commands.command(aliases=['lair'])
    async def showLair(self,ctx,user_to_show = None):
        """Displays a list of all chorumfurs in an @mentioned user's lair.
        If no user is supplied, returns your lair as always"""
        user_id = support_functions.strip_mention_format(user_to_show) if user_to_show else ctx.message.author.id
        returned_creatures = database_methods.get_my_creatures_from_db(user_id) or None
        if returned_creatures:
            msg_list = support_functions.format_output("{} - {}\n",
                                                      ("ID#","Creature Name"),
                                                       returned_creatures)
            for msg in msg_list:
                await ctx.send(msg)
            await ctx.send("**For more information run `.getCreature <Creature ID>`**")
        else:
            await ctx.send("No Chorumfurs Found")

async def setup(bot):
    await bot.add_cog(CreaturesCog(bot))