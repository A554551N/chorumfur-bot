import random
from decimal import Decimal
from discord.ext import commands
import database_methods
import support_functions
import forage_outcomes
import limited_time_events

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
            msg = ""
            if outcome.type == 'event_curr':
                msg = outcome.text.format(limited_time_events.march_event.event_currency_name)
                database_methods.add_item_to_user(ctx.author.id,limited_time_events.march_event.event_currency_id)
                
            elif outcome.type == 'lure':
                msg = outcome.text
                if outcome.reward is not None:
                    msg += f'\nChorumfur #{outcome.reward} has decided to join your lair!'
                    lured_chorumfur = database_methods.get_creature_from_db(outcome.reward)
                    lured_chorumfur.owner = ctx.author.id
                    database_methods.update_creature(lured_chorumfur)
                else:
                    wild_chorumfurs = database_methods.get_wild_chorumfur_ids()
                    if not wild_chorumfurs:
                        msg += "\nIt ran away, though."
                    else:
                        random_selection = random.randint(0,len(wild_chorumfurs)-1)
                        chorumfur_to_add = database_methods.get_creature_from_db(wild_chorumfurs[random_selection][0])
                        chorumfur_to_add.owner = ctx.author.id
                        database_methods.update_creature(chorumfur_to_add)
                        msg += f'\nChorumfur #{chorumfur_to_add.creatureId} has decided to join your lair!'

            elif outcome.type == 'currency':
                msg=outcome.text.format(creature.name,outcome.reward)
                database_methods.update_currency_in_wallet(ctx.author.id,outcome.reward)

            elif outcome.type == 'text':
                msg = outcome.text.format(creature.name)
            await ctx.send(f"{creature.name} is foraging!\n{msg}")
            await ctx.send(f"---DEBUG---\n{outcome.text}\n"\
                           f"Event Type: {outcome.type}\n"\
                            f"Reward: {outcome.reward}")

async def setup(bot):
    await bot.add_cog(ActivitiesCog(bot))
