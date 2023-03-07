from decimal import Decimal
import random
from Creature import Creature
from ConstantData import Constants

class Breeding:
    """A class to represent a proposed pairing of two creatures
       
       Attributes
       ----------
       creature_a: Creature
            a creature object that becomes parent A
       creature_b: Creature
            a creature object that becomes parent B
        new_creature_owner: int
            a user ID to assign to new creatures created by this Breeding
        parents_of_a: tuple
            an up-to-2-element tuple containing creature objects representing parents of creature_a
        parents_of_b: tuple
            an up-to-2-element tuple containing creature objects representing parents of creature_b
        
        Methods
        --------
        breed()
            produces a variable number of Creature objects with randomized traits based on parents
        select_trait_to_pass()
            chooses a trait from the available options to pass to a child
        """
    
    def __init__(self,creature_a,creature_b,new_creature_owner,parents_of_a=None,parents_of_b=None):
        self.creature_a = creature_a
        self.creature_b = creature_b
        self.new_creature_owner = new_creature_owner
        if random.randint(1,2) == 1:
            self.parent_palette_id = creature_a.creatureId
        else:
            self.parent_palette_id = creature_b.creatureId
        self.new_creature_generation = max(creature_a.generation,creature_b.generation)+1
        self.parents_of_a = parents_of_a
        self.parents_of_b = parents_of_b

    def breed(self):
        """Performs the breed action, producing randomized traits based on parents
        creature_a and creature_b.  Returns an array of Creatures."""
        # This is where weighting happens.
        number_of_pups = 0
        palette_choices = ["Parent A","Parent B","Mixed"]
        random_count_roll = Decimal(str(random.random()))
        for current_count in Constants.PUP_WEIGHTING:
            pup_weight = Decimal(Constants.PUP_WEIGHTING[current_count])
            if random_count_roll > pup_weight:
                random_count_roll -= pup_weight
            else:
                number_of_pups = current_count
                break
        pups = []
        for pup_count in range(1,(number_of_pups+1)):
            palette = palette_choices[random.randint(0,2)]
            pup = Creature(name=f"Pup {pup_count}",
                           owner=self.new_creature_owner,
                           generation=self.new_creature_generation,
                           palette=palette)
            for trait in pup.traits:
                pup.traits[trait] = self.select_trait_to_pass(trait)
            pups.append(pup)
        return pups

    def select_trait_to_pass(self,trait_type):
        """Selects a trait to pass to new pup.  Takes in a Trait_type and returns a string"""
        if random.randint(1,100) <= Constants.GRANDPARENT_PASS_TRAITS:
            grandparent_choice = random.randint(1,4)
            if self.parents_of_a:
                if grandparent_choice == 1:
                    return self.parents_of_a[0].traits[trait_type]
                return self.parents_of_a[1].traits[trait_type]
            if self.parents_of_b:
                if grandparent_choice == 3:
                    return self.parents_of_b[0].traits[trait_type]
                return self.parents_of_b[1].traits[trait_type]
        parent_choice = random.randint(1,2)
        if parent_choice == 1:
            return self.creature_a.traits[trait_type]
        return self.creature_b.traits[trait_type]

if __name__ == '__main__':
    for i in range(1000):
        print(random.randint(0,2))