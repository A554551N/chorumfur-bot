from decimal import Decimal
import random
from Creature import Creature
from ConstantData import Constants

class Breeding:
    """A class to represent a proposed pairing of two creatures"""
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
            pup = Creature(name=f"Pup {pup_count}",
                           owner=self.new_creature_owner,
                           generation=self.new_creature_generation)
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
    parent_a = Creature('parent a',1)
    parent_a.randomize_creature()
    parent_b = Creature('parent b',1)
    parent_b.randomize_creature()
    number_of_pups = {1:0,2:0,3:0,4:0}
    number_of_tests = 1000
    test_breed = Breeding(parent_a,parent_b,1)
    for test in range(number_of_tests):
        spawn = test_breed.breed()
        number_of_pups[len(spawn)] += 1
    print(number_of_pups)