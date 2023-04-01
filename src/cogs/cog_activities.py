from datetime import datetime
import random
from discord.ext import commands
from ConstantData import Constants
import database_methods
import support_functions
import forage_outcomes
import limited_time_events
from random import randint

class ActivitiesCog(commands.GroupCog, name='Activities', group_name='activities'):
    """Cog to group commands related to activities for players"""
    def __init__(self, bot):
        self.client = bot

    #FOR APRIL FOOLS ONLY
    @commands.command()
    async def cleanLitterBox(self,ctx):
        """Cleans all the litter boxes in a user's lair"""
        random_num = randint(1,100)
        if random_num >= 95:
            await ctx.send("You accidentally touch the poop while scooping...gross.")
        await ctx.send("Wow that was a lot of poop!  It's clean until tomorrow now at least.")

    @commands.command()
    async def feedChorumfur(self,ctx,creature_id):
        random_num = randint(1,10)
        creature = database_methods.get_creature_from_db(creature_id)
        if random_num == 10:
            await ctx.send(f"{creature.name} turns its nose up at delicious food.")
        else:
            await ctx.send(f"{creature.name} eats a delicious food right from your hand.  They make a happy noise!")

    @commands.command()
    async def eventScoreboard(self,ctx):
        """Displays all users and quantities of event currency collected"""

        returned_rows = database_methods.get_event_currency_leaderboard(29)
        output_list=[]
        for row in returned_rows:
            output_list.append((self.client.get_user(row[0]).name,row[1]))
        messages = support_functions.format_output('{} - {}\n',('User','Quantity'),output_list)
        for msg in messages:
            await ctx.send(msg)

    @commands.command(aliases=['f'])
    async def forage(self,ctx,creature_id):
        """Allows user chorumfurs to go on an adventure and discover something interesting
        
        Parameters
        ----------
        creature_id : int
            The ID of the creature that is foraging
        """
        creature = database_methods.get_creature_from_db(creature_id) or None
        can_forage = self.creature_can_forage(creature,ctx.author.id)
        if can_forage[0]:
            creature.last_forage = datetime.today()
            database_methods.update_creature(creature)
            subtype = support_functions.roll_random_result(forage_outcomes.outcome_types)
            possible_outcomes = forage_outcomes.outcome_subtypes[subtype]
            outcome = support_functions.roll_random_result(possible_outcomes)
            print(f"User: {ctx.author.name}\n"\
                  f"Type: {subtype}\n"\
                  f"Outcome Text: {outcome.text}\n"\
                  f"Outcome Type: {outcome.type}\n"\
                  f"Outcome Reward: {outcome.reward}")
            msg = ""
            if outcome.type == 'event_curr':
                msg = outcome.text.format(curr_name = limited_time_events.march_event.event_currency_name,
                                          amount=outcome.reward,
                                          creature_name=creature.name)
                database_methods.add_item_to_user(ctx.author.id,
                                                  limited_time_events.march_event.event_currency_id,
                                                  outcome.reward)
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
                msg=outcome.text.format(creature_name=creature.name,amount=outcome.reward)
                database_methods.update_currency_in_wallet(ctx.author.id,outcome.reward)

            elif outcome.type == 'text':
                msg = outcome.text.format(creature_name=creature.name,random_npc=Constants.NPCS[random.randint(0,len(Constants.NPCS)-1)])
            
            elif outcome.type == 'item':
                msg = outcome.text.format(creature_name=creature.name)
                database_methods.add_item_to_user(ctx.author.id,outcome.reward.item_id,outcome.reward.quantity)
            await ctx.send(f"{creature.name} is foraging!\n{msg}")
        else:
            await ctx.send(can_forage[1])

    def creature_can_forage(self,creature,user_id):
        """Checks to see if the creature meets the requirements to forage.
        Parameters
        ----------
        creature: Creature
            the creature to validate
        user_id: int
            the ID of the user running the command"""
        msg = ""
        time_delta = None
        if creature.last_forage:
            time_delta = datetime.today() - creature.last_forage
        valid = True
        if creature.owner != user_id:
            msg = "You can only send chorumfurs you own to forage."
            valid = False
        elif not creature.is_active:
            msg = "Only the chorumfurs in your party can forage."
            valid = False
        elif creature.last_forage and (time_delta.days == 0 and time_delta.seconds//3600 < Constants.FORAGE_COOLDOWN_HOURS):
            msg = "Each chorumfur can only forage once every six hours.  "\
                  f"You can forage again in {Constants.FORAGE_COOLDOWN_HOURS - time_delta.seconds//3600} hour(s)"
            valid = False
        return (valid,msg)
    
async def setup(bot):
    await bot.add_cog(ActivitiesCog(bot))
