from random import randint
from Creature import Creature
from ConstantData import Constants

class Breeding:
    """A class to represent a proposed pairing of two creatures"""
    def __init__(self,creature_a,creature_b,new_creature_owner,parents_of_a=None,parents_of_b=None):
        self.creature_a = creature_a
        self.creature_b = creature_b
        self.new_creature_owner = new_creature_owner
        if randint(1,2) == 1:
            self.parent_palette_id = creature_a.creatureId
        else:
            self.parent_palette_id = creature_b.creatureId
        self.new_creature_generation = max(creature_a.generation,creature_b.generation)+1
        self.parents_of_a = parents_of_a
        self.parents_of_b = parents_of_b

    def breed(self):
        """Performs the breed action, producing randomized traits based on parents
        creature_a and creature_b.  Returns an array of Creatures."""
        number_of_pups =  randint(1,4)
        pups = []
        for pup_count in range(1,(number_of_pups+1)):
            pup = Creature(name=f"Pup {pup_count}",
                           owner=self.new_creature_owner,
                           generation=self.new_creature_generation)
            for trait in pup.traits:
                pup.traits[trait] = self.select_trait_to_pass(trait)
            pups.append(pup)
            print(pups[len(pups)-1].outputCreature())
        for test_pup in pups:
            print(test_pup.outputCreature())
        return pups

    def select_trait_to_pass(self,trait_type):
        """Selects a trait to pass to new pup.  Takes in a Trait_type and returns a string"""
        if randint(1,100) <= Constants.GRANDPARENT_PASS_TRAITS:
            grandparent_choice = randint(1,4)
            if self.parents_of_a:
                if grandparent_choice == 1:
                    return self.parents_of_a[0].traits[trait_type]
                return self.parents_of_a[1].traits[trait_type]
            if self.parents_of_b:
                if grandparent_choice == 3:
                    return self.parents_of_b[0].traits[trait_type]
                return self.parents_of_b[1].traits[trait_type]
        parent_choice = randint(1,2)
        if parent_choice == 1:
            return self.creature_a.traits[trait_type]
        return self.creature_b.traits[trait_type]

if __name__ == '__main__':
    parent_a = Creature('parent a',1)
    parent_a.randomize_creature()
    print(parent_a.outputCreature())
    parent_b = Creature('parent b',1)
    parent_b.randomize_creature()
    print(parent_b.outputCreature())
    test_breed = Breeding(parent_a,parent_b,1)
    spawn = test_breed.breed()
    #for pup in spawn:
        #print(pup.outputCreature())