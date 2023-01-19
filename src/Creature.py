from datetime import datetime
from random import randint
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
    def __init__(self,name,owner,traits={},imageLink = "",generation=0,creatureId=None,createDate=None,ownerName=None):
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

    def randomize_creature_weighted(self,configuration_dict):
        """Selects an option from a given set of weights"""
        summed_weight = 0
        for item in configuration_dict.values():
            summed_weight += item[1]
        roll = randint(1,summed_weight)
        for item in configuration_dict:
            weight = configuration_dict[item][1]
            if roll > configuration_dict[item][1]:
                roll -= weight
            else:
                return item


    
    def outputCreature(self):
        age = datetime.today() - self.createDate
        output = f"ID: {self.creatureId}\n"\
                f"Name: {self.name}\n"\
                f"Owner: {self.ownerName}\n"\
                f"Age: {age}\n"\
                f"Create Date: {datetime.strftime(self.createDate,Constants.DATEONLYFORMAT)}\n"\
                f"Generation: {self.generation}\n"
        return output

if __name__ == '__main__':
    new_creature = Creature("a",1)
    results_dict = {}
    for i in range(1000):
        key_result = new_creature.randomize_creature_weighted(Constants.MAIN_HORN)
        if key_result in results_dict:
            results_dict[key_result] += 1
        else:
            results_dict[key_result] = 1
    print(results_dict)