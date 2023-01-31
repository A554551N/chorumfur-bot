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
        generation: int
            incremented from parent

        Methods
        ---------
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
                parents=[None,None]):
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


    def outputCreature(self):
        """Returns a tuple containing a formatted string with details about the
        creature and the correct image for the bot to display based on the creature's age.
        The amount of information returned in the string also varies based on creature's age."""
        age = datetime.today() - self.createDate
        image_link = ""
        output = f"**ID:** {self.creatureId}\n"\
                f"**Name:** {self.name}\n"\
                f"**Owner:** {self.ownerName}\n"\
                f"**Age:** {age}\n"\
                f"**Create Date:** {datetime.strftime(self.createDate,Constants.DATEONLYFORMAT)}\n"\
                f"**Generation:** {self.generation}\n"\
                 "**---Traits---**\n"
        if age.days <= 7 and self.generation != 0:
            image_link = self.imageLink_nb
        elif age.days <= 14 and self.generation != 0:
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
