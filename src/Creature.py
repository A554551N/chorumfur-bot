from datetime import datetime
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
    def __init__(self,name,owner,imageLink = "",generation=0,creatureId=None,createDate=None,ownerName=None):
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
    
    def outputCreature(self):
        age = datetime.today() - self.createDate
        output = f"ID: {self.creatureId}\n"\
                f"Name: {self.name}\n"\
                f"Owner: {self.ownerName}\n"\
                f"Age: {age}\n"\
                f"Create Date: {datetime.strftime(self.createDate,Constants.DATEONLYFORMAT)}\n"\
                f"Generation: {self.generation}\n"\
                f"Image: {self.imageLink}"
        return output