import math
from datetime import datetime
from ConstantData import Constants
class User:
    """
        A class to represent a User

        Attributes
        ----------
        userId : integer
            Unique Discord ID for User
        name : string
            a friendly name for User
        level : integer
            User's level (currently unused)
        wallet : integer
            A user's quantity of money
        inventory : dict (itemId : (Item object,quantity integer))
            all inventory items currently associated with this user and their quantity.
        lastBreed : datetime
            last date the breeding power was used
        warningsIssued : integer
            number of warnings issued to this user (currently unused)
        daysSinceLastBreed : timedelta
            determines time since last breeding
        is_breeding_pending : boolean
        BREEDINGSTONELINKS : dict
            dictionary containing links to Breeding Stone images
        Methods
        ---------
        outputProfile()
            returns a formatted string with the user's profile
        
        breedingLevel()
            returns an int (1-6) indicating User readiness for breeding
    """

    def __init__(self,userId,level=1,lastBreed=None,warningsIssued=0,name="",daysSinceLastBreed=None,wallet=0,is_breeding_pending=False):
        self.userId = userId
        self.name = name
        self.level = level
        self.wallet = wallet
        if lastBreed == "None":
            lastBreed = None
        elif isinstance(lastBreed,str):
            lastBreed = datetime.strptime(lastBreed,Constants.DATETIMEFORMAT)
            daysSinceLastBreed = (datetime.today() - lastBreed).days
        self.daysSinceLastBreed = daysSinceLastBreed
        self.lastBreed = lastBreed
        self.warningsIssued = warningsIssued
        self.is_breeding_pending = is_breeding_pending
    
    def breedingLevel(self,test=False):
        """
        calculates the breeding readiness of an account and returns an integer.
        Breeding level is calculated as follows:
        (in days) floor((today's date - last breed date)/5)
        """
        if test:
            today = datetime(2022,12,31)
        elif not self.lastBreed:
            return 5
        else:
            today = datetime.today()
        daysSinceLastBreed = today - self.lastBreed
        breedingLevel = math.floor(daysSinceLastBreed.days/6)
        if breedingLevel > 5:
            breedingLevel = 5
        elif breedingLevel < 0:
            breedingLevel = 0
        return breedingLevel
    
    def outputProfile(self):
        """outputs a profile string to display in server"""
        output = f"**{self.name}**\n"\
                f"**Level:** {self.level}\n"\
                f"**Last Breeding:** {self.lastBreed}\n"
        return output
    
    def daysUntilFull(self):
        """calculates how many days until the breeding crystal is ready to be used."""
        if self.lastBreed:
            daysUntilFull = datetime.today() - self.lastBreed
            if daysUntilFull.days < 0:
                return 0
            return 30 - self.daysSinceLastBreed
        return 0
    
    def update_last_breed(self):
        self.lastBreed = datetime.today()