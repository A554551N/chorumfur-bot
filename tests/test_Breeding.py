"""Tests for the Breeding class"""
import pytest
from .context import Creature
from .context import Breeding
from .context import database_methods

@pytest.fixture
def test_creature_a():
    creature = Creature(name='test_creature_a',owner=99999,generation=1)
    return creature

@pytest.fixture
def test_creature_b():
    creature = Creature(name='test_creature_b',owner=99999,generation=2)
    return creature

@pytest.fixture
def test_creature_c():
    creature = Creature(name='test_creature_c',owner=11111)
    return creature

def test_breed_same_owner_no_grandparents():
    test_creature_a = database_methods.get_creature_from_db(50)
    test_creature_b = database_methods.get_creature_from_db(39)
    test_breeding = Breeding(test_creature_a,test_creature_b,202632427535859712)
    assert test_breeding.breed()

def test_breed_same_owner_grandparents():
    test_creature_a = database_methods.get_creature_from_db(57)
    test_creature_b = database_methods.get_creature_from_db(55)
    test_gp_a = database_methods.get_parents_from_db(test_creature_a)
    test_gp_b = database_methods.get_parents_from_db(test_creature_b)
    test_breeding = Breeding(test_creature_a,test_creature_b,202632427535859712,test_gp_a,test_gp_b)
    assert test_breeding.breed()

def test_pup_weighting():
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
    # Assert assumes an expected value of 400 (40%) per thousand
    assert number_of_pups[2] <= 550 and number_of_pups[2] >= 350
