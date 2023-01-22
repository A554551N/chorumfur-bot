"""Tests for the Breeding class"""
import pytest
from .context import Creature
from .context import Breeding

@pytest.fixture
def test_creature_a():
    creature = Creature(name='test_creature_a',owner=99999)
    return creature

@pytest.fixture
def test_creature_b():
    creature = Creature(name='test_creature_b',owner=99999)
    return creature

@pytest.fixture
def test_creature_c():
    creature = Creature(name='test_creature_c',owner=11111)
    return creature

def test_breed_same_owner(test_creature_a,test_creature_b):
    test_breeding = Breeding(test_creature_a,test_creature_b)
    assert test_breeding.breed()