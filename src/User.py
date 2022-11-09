import datetime
import math
class User:
    """
        A class to represent a User

        Attributes
        ----------
        userId : integer
            Unique Discord ID for User
        level : integer
            User's level (currently unused)
        lastBreed : integer (Date)
            last date the breeding power was used
        warningsIssued : integer
            number of warnings issued to this user (currently unused)

        Methods
        ---------
        outputProfile()
            returns a formatted string with the user's profile
        
        breedingLevel()
            returns an int (1-6) indicating User readiness for breeding
    """
    def __init__(self,userId,level=1,lastBreed=None,warningsIssued=0):
        self.userId = userId
        self.level = level
        self.lastBreed = lastBreed
        self.warningsIssued = warningsIssued
    
    def breedingLevel(self,test=False):
        """
        calculates the breeding readiness of an account and returns an integer.
        Breeding level is calculated as follows:
        (in days) floor((today's date - last breed date)/5)
        """
        if test:
            today = datetime.datetime(2022,12,31)
        else:
            today = datetime.datetime.today()
        daysSinceLastBreed = today - self.lastBreed
        breedingLevel = math.floor(daysSinceLastBreed.days/6)
        if breedingLevel > 5:
            breedingLevel = 5
        elif breedingLevel < 0:
            breedingLevel = 0
        return breedingLevel
