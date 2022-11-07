import datetime
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
            createDate= datetime.datetime.today()
        else:
            createDate = datetime.datetime.strptime(createDate,'''%Y-%m-%d %H:%M:%S.%f''')
        self.owner = owner
        self.imageLink = imageLink
        self.generation = generation
        self.creatureId = creatureId
        self.createDate = createDate
    
    def outputCreature(self):
        age = datetime.datetime.today() - self.createDate
        output = f"ID: {self.creatureId}\n"\
                f"Name: {self.name}\n"\
                f"Owner: {self.owner}\n"\
                f"Age: {age}\n"\
                f"Create Date: {self.createDate}\n"\
                f"Generation: {self.generation}\n"\
                f"Image: {self.imageLink}"
        return output