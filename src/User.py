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
    def __init__(self):
        pass