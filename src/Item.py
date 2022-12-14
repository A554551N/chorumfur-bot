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

    Methods
    ---------
    outputItem()
        returns a formatted string with information about the Item
    """

    def __init__(self,name,description,value,imageLink="",id=None):
        self.name = name
        self.description = description
        self.value = value
        self.imageLink = imageLink
        self.id = id

    def outputItem(self):
        output = f"**{self.name}**\n"\
            f"{self.description}\n"\
            f"**Value:** {self.value}"
        return output