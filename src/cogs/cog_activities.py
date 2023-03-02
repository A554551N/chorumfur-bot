from random import random
from decimal import Decimal
from discord.ext import commands
import database_methods
import support_functions
import forage_outcomes

class ActivitiesCog(commands.GroupCog, name='Activities', group_name='activities'):
    """Cog to group commands related to activities for players"""

    @commands.command()
    async def forage(self,ctx,creature_id):
        """Allows user chorumfurs to go on an adventure and discover something interesting
        
        Parameters
        ----------
        creature_id : int
            The ID of the creature that is foraging
        """
        creature = database_methods.get_creature_from_db(creature_id) or None
        if creature.owner != ctx.author.id:
            await ctx.send("You can only send chorumfurs from your lair to forage")
        else:
            subtype = support_functions.roll_random_result(forage_outcomes.outcome_types)
            possible_outcomes = forage_outcomes.outcome_subtypes[subtype]
            outcome = support_functions.roll_random_result(possible_outcomes)
            await ctx.send(f"{creature.name} is foraging!\n{outcome.text}\n"\
                           f"Event Type: {outcome.type}\n"\
                            f"Reward: {outcome.reward}")

async def setup(bot):
    await bot.add_cog(ActivitiesCog(bot))
