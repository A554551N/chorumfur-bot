import time
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
        imageLink: string
            link to an image of the creature
        generation: int
            incremented from parent

        Methods
        ---------
        outputCreature()
            returns a formatted string with date about creature
    """
    def __init__(self,name,owner,imageLink = "",generation=0,creatureId=None,createDate=None):
        self.name = name
        if not createDate:
            createDate= time.localtime()
        self.owner = owner
        self.imageLink = imageLink
        self.generation = generation
        self.creatureId = creatureId
        self.createDate = createDate
    
    def outputCreature(self):
        output = f"ID: {self.creatureId}\n"\
                f"Name: {self.name}\n"\
                f"Owner: {self.owner}\n"\
                f"Create Date: {self.createDate}\n"\
                f"Generation: {self.generation}"
        return output