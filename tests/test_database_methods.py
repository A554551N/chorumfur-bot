"""Includes tests to ensure the database is functioning"""
import pytest
import random
from .context import database_methods

@pytest.fixture
def random_user_constants():
    return {'user_id' : random.randint(1,1000000),
    'user_level' : random.randint(1,99),
    'user_wallet' : random.randint(1,1000000),
    'user_last_breed' : 'date',
    'user_warnings_issued' : random.randint(1,100)
    }
def test_database_connection_prod():
    """Tests to confirm that a database connetion is successfully formed."""
    assert database_methods.is_database_connected()

def test_add_user_to_database(random_user_constants):
    """Tests to confirm that a user can be added to the users database"""
    assert database_methods.add_user_to_database(
        user_id = random_user_constants['user_id'],
        user_level = random_user_constants['user_level'],
        user_wallet = random_user_constants['user_wallet'],
        user_last_breed = random_user_constants['user_last_breed'],
        user_warnings_issued = random_user_constants['user_warnings_issued']
    )