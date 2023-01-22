from Creature import Creature

class Breeding:
    """An class to represent a proposed pairing of two creatures"""
    def __init__(self,creature_a,creature_b):
        self.creature_a = creature_a
        self.creature_b = creature_b
    
    def has_same_owner(self):
        """Determines whether creature_a and creature_b has same owner.  Returns True/False"""
        if self.creature_a.owner == self.creature_b.owner:
            return True
        return False