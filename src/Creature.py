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
        date: array
            Date creature instantiated stored as a year/month/day array
        owner: int
            User ID of the creating user
        imageLink: string
            link to an image of the creature
        generation: int
            incremented from parent
        isNew: bool
            flagged if this is a new creature (false by default)

    """
    def __init__(self,name,owner,imageLink = "",generation=0,creatureId=None,date=None,isNew=False):
        self.name = name
        if isNew:
            date= time.localtime()
            self.createDate = [date.tm_year,date.tm_mon,date.tm_mday]
        else:
            self.createDate = date
        self.owner = owner
        self.imageLink = imageLink
        self.generation = generation
        print(generation)
        self.creatureId = creatureId
    
    def outputCreature(self):
        output = f"ID: {self.creatureId}\n"\
                f"Name: {self.name}\n"\
                f"Owner: {self.owner}\n"\
                f"Create Date: {self.createDate[1]} {self.createDate[2]} {self.createDate[0]}\n"\
                f"Generation: {self.generation}"
        return output