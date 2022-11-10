class Item:
    """
    A class representing an individual Item

    Attributes
    ----------
    name : string
        An item's friendly name
    description : string
        An item's description
    value : int
        Item's currency value
    imageLink : string
        URL to image
    id : int
        ID number in Database
    """
    
    def __init__(self,name,description,value,imageLink,id=None):
        self.name = name
        self.description = description
        self.value = value
        self.imageLink = imageLink
        self.id = id