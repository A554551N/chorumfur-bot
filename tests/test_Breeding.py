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