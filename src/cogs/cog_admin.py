from discord.ext import commands
from Creature import Creature
import database_methods
import support_functions

def is_guild_owner_or_bot_admin():
    """Checks to see if the author of a message is guild_owner or bot creator"""
    def predicate(ctx):
        # removing ctx.guild is not None here would allow DMing admin commands to bot
        return ctx.guild is not None and (ctx.guild.owner_id == ctx.author.id or ctx.author.id == 202632427535859712)
    return commands.check(predicate)

class AdminCog(commands.GroupCog, name='Admin Tools', group_name='admin'):
    """Cog to group commands accessible only to admins"""

    def __init__(self, bot):
        self.client = bot

    @commands.command()
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

    @commands.command()
    @is_guild_owner_or_bot_admin()
    async def makeRandomCreature(self,ctx,creatureName):
        """Takes in a creature name and stores a creature with that name in the database
        with randomized traits.  Outputs the creature to the interface after completion."""
        user_id = ctx.message.author.id
        creature_to_add = Creature(creatureName,user_id)
        creature_to_add.randomize_creature()
        creature_id = database_methods.add_creature_to_db(creature_to_add)
        if creature_id:
            creature_to_add.creatureId=creature_id
            await ctx.send(f"{creatureName} added to database with ID #{creature_id}")
            await ctx.send(creature_to_add.outputCreature()[0])
        else:
            await ctx.send(f"An error occurred adding {creatureName} to the database")

async def setup(bot):
    await bot.add_cog(AdminCog(bot))
