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
        createDate: date
            Date Creature Object was instantiated
        owner: int
            User ID of the creating user
        generation: int
            incremented from parent

    """
    def __init__(self,name,owner,generation=0,creatureId=0,date=time.localtime()):
        self.name = name
        self.createDate = [date.tm_year,date.tm_mon,date.tm_mday]
        self.owner = owner
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