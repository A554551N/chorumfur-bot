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
    def __init__(self,name,owner,traits=Constants.DEFAULT_TRAITS_DICT,
                imageLink = "No Image",generation=0,creatureId=None,createDate=None,ownerName=None):
        self.name = name
        if not createDate:
            createDate= datetime.today()
        else:
            createDate = datetime.strptime(createDate,Constants.DATETIMEFORMAT)
        self.owner = owner
        self.ownerName = ownerName
        self.imageLink = imageLink
        self.generation = generation
        self.creatureId = creatureId
        self.createDate = createDate
        self.traits = traits

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
                random_roll = random_roll - trait_weight
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
        age = datetime.today() - self.createDate
        output = f"ID: {self.creatureId}\n"\
                f"Name: {self.name}\n"\
                f"Owner: {self.ownerName}\n"\
                f"Age: {age}\n"\
                f"Create Date: {datetime.strftime(self.createDate,Constants.DATEONLYFORMAT)}\n"\
                f"Generation: {self.generation}\n"\
                f"Main Horn: {Constants.MAIN_HORN[self.traits['MAIN_HORN']][0]}\n"\
                f"Cheek Horn: {Constants.CHEEK_HORN[self.traits['CHEEK_HORN']][0]}\n"\
                f"Face Horn: {Constants.FACE_HORN[self.traits['FACE_HORN']][0]}\n"\
                f"Tail: {Constants.TAIL[self.traits['TAIL']][0]}\n"\
                f"Tail Tip: {Constants.TAIL_TIP[self.traits['TAIL_TIP']][0]}\n"\
                f"Fluff: {Constants.FLUFF[self.traits['FLUFF']][0]}\n"\
                f"Mutation: {Constants.MUTATION[self.traits['MUTATION']][0]}\n"
        return output

if __name__ == '__main__':

    number_runs = 10000
    new_creature = Creature("a",1)
    total_mutations = 0
    main_horns = {}
    for i in range(number_runs):
        new_creature.randomize_creature()
        if new_creature.traits['MAIN_HORN'] in main_horns:
            main_horns[new_creature.traits['MAIN_HORN']] += 1
        else: main_horns[new_creature.traits['MAIN_HORN']] = 1
        if new_creature.traits['MUTATION'] != 1:
            total_mutations += 1
            print("Mutation Detected")
    print(main_horns)
    print(f"Total runs: {number_runs}\nMutations Discovered: {total_mutations}")
