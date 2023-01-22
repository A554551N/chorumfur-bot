from random import randint
from Creature import Creature
import database_methods
from ConstantData import Constants

class Breeding:
    """An class to represent a proposed pairing of two creatures"""
    def __init__(self,creature_a,creature_b,new_creature_owner):
        self.creature_a = creature_a
        self.creature_b = creature_b
        self.new_creature_owner = new_creature_owner
        if randint(1,2) == 1:
            self.parent_palette_id = creature_a.creatureId
        else:
            self.parent_palette_id = creature_b.creatureId
        self.new_creature_generation = max(creature_a.generation,creature_b.generation)+1
        self.parents_of_a = None
        self.parents_of_b = None
        if creature_a.generation >= 2:
            self.parents_of_a = database_methods.get_parents_from_db(self.creature_a)
        if creature_b.generation >= 2:
            self.parents_of_b = database_methods.get_parents_from_db(self.creature_b)

    def creatures_have_same_owner(self):
        """Determines whether creature_a and creature_b has same owner.  Returns True/False"""
        if self.creature_a.owner == self.creature_b.owner:
            return True
        return False
    
    def breed(self):
        """Performs the breed action, producing randomized traits based on parents
        creature_a and creature_b"""
        if self.creatures_have_same_owner():
            number_of_pups = randint(1,4)
            added_creature_ids = []
            for pup_count in range(1,(number_of_pups+1)):
                pup = Creature(name=f"Pup {pup_count}",
                               owner=self.new_creature_owner,
                               generation=self.new_creature_generation)
                for trait in Constants.DEFAULT_TRAITS_DICT:
                    pup.traits[trait] = self.select_trait_to_pass(trait)
                added_creature_ids.append(database_methods.add_creature_to_db(pup))
            return added_creature_ids
        return None
    
    def select_trait_to_pass(self,trait_type):
        """Selects a trait to pass to new pup.  Takes in a Trait_type and returns a string"""
        if randint(1,100) <= Constants.GRANDPARENT_PASS_TRAITS:
            grandparent_choice = randint(1,4)
            if self.parents_of_a:
                if grandparent_choice == 1:
                    return self.parents_of_a[0].traits[trait_type]
                elif grandparent_choice == 2:
                    return self.parents_of_a[1].traits[trait_type]
            if self.parents_of_b:
                if grandparent_choice == 3:
                    return self.parents_of_b[0].traits[trait_type]
                else:
                    return self.parents_of_b[1].traits[trait_type]
        parent_choice = randint(1,2)
        if parent_choice == 1:
            return self.creature_a.traits[trait_type]
        else:
            return self.creature_b.traits[trait_type]
