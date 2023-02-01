from discord.ext import commands
import database_methods

class CreaturesCog(commands.GroupCog, name='Chorumfur Management',group_name='chorumfurs'):
    """Cog to group commands related to managing creatures"""
    def __init__(self,bot):
        self.client = bot

    def strip_mention_format(self,mention):
        """removes leading <@ and trailing > from user IDs passed as mentions"""
        return mention[2:-1]

    @commands.command(aliases=['gc','getcreature'],require_var_positional=True)
    async def getCreature(self,ctx,creatureId):
        """Takes in a creature ID and sends a formatted output of the creature to discord"""
        requested_creature = database_methods.get_creature_from_db(creatureId)
        if requested_creature:
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
            creature_to_give.owner = self.strip_mention_format(new_owner)
        if database_methods.update_creature(creature_to_give):
            await ctx.send("Creature has been given to requested user.")
        else:
            await ctx.send("An error has occurred, your creature has not been transferred.")


async def setup(bot):
    await bot.add_cog(CreaturesCog(bot))
