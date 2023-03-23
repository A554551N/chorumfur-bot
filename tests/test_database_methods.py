"""Includes tests to ensure the database is functioning"""
import random
import pytest
from datetime import datetime
from .context import User
from .context import Item
from .context import database_methods

@pytest.fixture
def random_user_constants():
    """creates random user data for test methods"""
    return {'user_id' : random.randint(1,1000000),
    'user_level' : random.randint(1,99),
    'user_wallet' : random.randint(1,1000000),
    'user_last_breed' : datetime.today(),
    'user_warnings_issued' : random.randint(1,100)
    }
def test_database_connection():
    """Tests to confirm that a database connetion is successfully formed."""
    assert database_methods.is_database_connected()

def test_reject_duplicate_user_id(random_user_constants):
    """Tests to confirm that the database correctly rejects a duplicate user."""
    user_to_add = User(userId=99999,
                       level=random_user_constants['user_level'],
                       wallet=random_user_constants['user_wallet'],
                       lastBreed=random_user_constants['user_last_breed'],
                       warningsIssued=random_user_constants['user_warnings_issued'])
    assert not database_methods.add_user_to_database(user_to_add)

def test_add_user_to_database(random_user_constants):
    """Tests to confirm that a user can be added to the users database"""
    user_to_add = User(userId=random_user_constants['user_id'],
                       level=random_user_constants['user_level'],
                       wallet=random_user_constants['user_wallet'],
                       lastBreed=random_user_constants['user_last_breed'],
                       warningsIssued=random_user_constants['user_warnings_issued'])
    assert database_methods.add_user_to_database(user_to_add)

def test_add_user_with_defaults(random_user_constants):
    """Tests to confirm that the database correctly rejects a duplicate user."""
    user_to_add = User(random_user_constants['user_id'])
    assert database_methods.add_user_to_database(user_to_add)

def test_add_item_to_user():
    """Tests to confirm an item can be added to owned_items and associated to a user"""
    assert database_methods.add_item_to_user(99999,1)

def test_remove_item_from_user():
    """Tests to confirm items can be removed from a user in owned_items"""
    database_methods.add_item_to_user(99999,2)
    assert database_methods.remove_item_from_user(99999,2)

def test_cannot_remove_unowned_item():
    """Tests to confirm that items not associated with a user are not removed"""
    assert not database_methods.remove_item_from_user(99999,1000)

def test_get_item_from_db():
    """Tests to confirm that an item can be retreived from the database"""
    test_item = database_methods.get_item_from_db(1)
    assert test_item.id == 1

def test_cannot_get_nonexistant_item():
    """Tests to confirm that get_item_from_db fails gracefully on no record"""
    assert not database_methods.get_item_from_db(999999)

def test_get_user_inventory():
    """Tests that a user can retreive their inventory"""
    returned_inventory = database_methods.get_user_inventory(99999)
    assert returned_inventory[0][1] == "Beach Fun"
    