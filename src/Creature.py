from datetime import datetime
import random
from decimal import Decimal
from ConstantData import Constants
class Creature:
    """
        A class to represent a Creature

        Attributes
        ----------
        creatureId : int
            creatureID created by database
        name: string
            name of the creature
        createDate : Date
            Date creature was created
        owner: int
            User ID of the creating user
        ownerName: string
            Friendly name for Creature Owner
        imageLink: string
            link to an image of the creature
        imageLink_nb: string
            link to an image of the creature as a newborn
        imageLink_pup: string
            link to an image of the creature as a pup
        generation: int
            incremented from parent
        parents: list
            IDs indicating a chorumfur's parents (not applicable to Gen 0)
        avaialable_to_breed: bool
            True if creature should appear in .matingDance, otherwise False
        palette: string
            which parent's pallet to apply for art
        is_active: bool
            True if creature is active in a user's party, otherwise False
        last_forage: datetime
            Datetime when this creature was last used to .forage

        Methods
        ---------
        randomize_trait()
            selects a trait from a list of possibilities and returns it
        randomize_creature()
            replaces a creatures traits with random ones
        calculate_age()
            determines a creature's age based on creation date
        outputCreature()
            returns a formatted string with date about creature
    """
    def __init__(self,name,owner,
                traits=Constants.DEFAULT_TRAITS_DICT,
                imageLink = "No Image",
                imageLink_nb = "No Image",
                imageLink_pup = "No Image",
                generation=0,
                creatureId=None,
                createDate=None,
                ownerName=None,
                parents=[None,None],
                available_to_breed=False,
                palette="N/A",
                is_active=False,
                last_forage=None):
        self.name = name
        if not createDate:
            createDate= datetime.today()
        else:
            createDate = datetime.strptime(createDate,Constants.DATETIMEFORMAT)
        self.owner = owner
        self.ownerName = ownerName
        # Confirm whether this is still necessary
        if imageLink:
            self.imageLink = imageLink
        else:
            self.imageLink = "No Image"
        self.imageLink_nb = imageLink_nb
        self.imageLink_pup = imageLink_pup
        self.generation = generation
        self.creatureId = creatureId
        self.createDate = createDate
        self.traits = dict(traits)
        self.parents = parents
        self.available_to_breed = available_to_breed
        self.palette = palette
        self.is_active = is_active
        self.last_forage = last_forage

    def randomize_trait(self,trait_category):
        """Takes in a trait category and returns a randomly selected trait"""
        sum_of_options = 0
        for trait_type_weights in trait_category.values():
            sum_of_options += Decimal(trait_type_weights)
        if sum_of_options != 1:
            return None
        random_roll = Decimal(str(random.random()))
        for trait_type in trait_category:
            trait_weight = Decimal(trait_category[trait_type])
            if random_roll > trait_weight:
                random_roll -= trait_weight
            else:
                return trait_type

    def randomize_creature(self):
        """randomize the traits of this creature by replacing self.traits with a random dict"""
        random_traits={}
        random_traits['MAIN_HORN'] = self.randomize_trait(Constants.MAIN_HORN)
        random_traits['CHEEK_HORN'] = self.randomize_trait(Constants.CHEEK_HORN)
        random_traits['FACE_HORN'] = self.randomize_trait(Constants.FACE_HORN)
        random_traits['TAIL'] = self.randomize_trait(Constants.TAIL)
        random_traits['TAIL_TIP'] = self.randomize_trait(Constants.TAIL_TIP)
        random_traits['FLUFF'] = self.randomize_trait(Constants.FLUFF)
        random_traits['MUTATION'] = self.randomize_trait(Constants.MUTATION)
        self.traits = random_traits

    def calculate_age(self):
        """Calculates the Creature's age based on its create date and returns the value as a time_delta"""
        return datetime.today() - self.createDate

    def outputCreature(self,output_all = False):
        """Returns a tuple containing a formatted string with details about the
        creature and the correct image for the bot to display based on the creature's age.
        The amount of information returned in the string also varies based on creature's age."""
        age = self.calculate_age()
        print(self.parents)
        if self.parents[0] and self.parents[1]:
            parent_string = f"{self.parents[0].creatureId} - {self.parents[0].name} & "\
                            f"{self.parents[1].creatureId} - {self.parents[1].name}"
        else:
            parent_string = 'No Parents Found'
        image_link = ""
        output = f"**ID:** {self.creatureId}\n"\
                f"**Name:** {self.name}\n"\
                f"**Owner:** {self.ownerName}\n"\
                f"**Age:** {age}\n"\
                f"**Create Date:** {datetime.strftime(self.createDate,Constants.DATEONLYFORMAT)}\n"\
                f"**Parents:** {parent_string}\n"\
                f"**Generation:** {self.generation}\n"
        output += f"**Palette:** {self.palette}\n" if output_all and hasattr(self,'palette') else ""
        output += "**---Traits---**\n"
        if age.days <= 7 and self.generation != 0 and not output_all:
            image_link = self.imageLink_nb
        elif age.days <= 14 and self.generation != 0 and not output_all:
            output += f"**Main Horn**: {self.traits['MAIN_HORN']}\n"
            image_link = self.imageLink_pup
        else:
            output +=f"**Main Horn**: {self.traits['MAIN_HORN']}\n"\
                     f"**Cheek Horn**: {self.traits['CHEEK_HORN']}\n"\
                     f"**Face Horn**: {self.traits['FACE_HORN']}\n"\
                     f"**Tail**: {self.traits['TAIL']}\n"\
                     f"**Tail Tip**: {self.traits['TAIL_TIP']}\n"\
                     f"**Fluff**: {self.traits['FLUFF']}\n"\
                     f"**Mutation**: {self.traits['MUTATION']}\n"
            image_link = self.imageLink
        return (output,image_link)

if __name__ == '__main__':
    test_creature_nb = Creature('test_nb',1,generation=1)
    test_creature_pup = Creature('test_pup',1,generation=1,createDate=datetime(2023,1,23).strftime(Constants.DATETIMEFORMAT))
    test_creature_adult = Creature('test_adult',1,generation=1,createDate=datetime(2022,12,31).strftime(Constants.DATETIMEFORMAT))
    print(test_creature_nb.outputCreature()[0])
    print("----------------------")
    print(test_creature_pup.outputCreature()[0])
    print("----------------------")
    print(test_creature_adult.outputCreature()[0])
