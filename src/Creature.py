from datetime import datetime
from ConstantData import Constants
from random import randint
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

    def randomize_creature(self):
        """Overwrites all trait fields with random values"""
        self.traits['MAIN_HORN'] = randint(1,len(Constants.MAIN_HORN))
        self.traits['CHEEK_HORN'] = randint(1,len(Constants.CHEEK_HORN))
        self.traits['FACE_HORN'] = randint(1,len(Constants.FACE_HORN))
        self.traits['TAIL'] = randint(1,len(Constants.TAIL))
        self.traits['TAIL_TIP'] = randint(1,len(Constants.TAIL_TIP))
        self.traits['FLUFF'] = randint(1,len(Constants.FLUFF))
        #if randint(1,100) <= Constants.CHANCE_TO_ADD_MUTATION:
        self.traits['MUTATION'] = randint(1,len(Constants.MUTATION))

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
    new_creature.randomize_creature()