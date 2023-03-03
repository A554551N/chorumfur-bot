from .context import User
from .context import database_methods
from .context import Item
from .context import Constants
import random
import pytest
from datetime import datetime

@pytest.fixture
def user_attributes():
    user_attributes = {
                    "ID" : random.randint(1,1000000),
                    "level" : 99,
                    "wallet" : 0,
                    "lastBreed" : datetime(2022,12,31),
                    "warningsIssued" : 0
                    }
    return user_attributes

@pytest.fixture
def createTestUser(user_attributes):
    testUser = User(userId=user_attributes["ID"],
                    level=user_attributes["level"],
                    lastBreed=user_attributes["lastBreed"],
                    warningsIssued=user_attributes["warningsIssued"],
                    wallet=user_attributes['wallet'])
    return testUser

def test_create_user_default(user_attributes):
    """Confirms that a user can be created by supplying only an"""
    test_user = User(user_attributes["ID"])
    assert test_user

def test_create_user_all_values(user_attributes):
    """Confirms that a user can be created with all values selected"""
    test_user = User(user_attributes["ID"],
                        user_attributes["level"],
                        user_attributes["lastBreed"],
                        user_attributes["warningsIssued"])
    assert test_user.userId == user_attributes["ID"]

def test_breeding_level_1(user_attributes):
    """Confirms that breeding level 1 is identified correctly"""
    testUser = User(user_attributes["ID"],
                        user_attributes["level"],
                        datetime(2022,12,31),
                        user_attributes["warningsIssued"])
    assert testUser.breedingLevel(True) == 0

def test_breeding_level_3(user_attributes):
    """Confirms that breeding level 3 is identified correctly"""
    testUser = User(user_attributes["ID"],
                        user_attributes["level"],
                        datetime(2022,12,19),
                        user_attributes["warningsIssued"])
    assert testUser.breedingLevel(True) == 2

def test_breeding_level_6(user_attributes):
    """Confirms that breeding level 6 is identified correctly"""
    testUser = User(user_attributes["ID"],
                        user_attributes["level"],
                        datetime(2022,11,30),
                        user_attributes["warningsIssued"])
    assert testUser.breedingLevel(True) == 5

def test_breeding_level_under_0(user_attributes):
    """Confirms that breeding levels less than 0 are set to 0"""
    testUser = User(user_attributes["ID"],
                        user_attributes["level"],
                        datetime(2023,1,1),
                        user_attributes["warningsIssued"])
    assert testUser.breedingLevel(True) == 0

def test_breeding_level_above_5(user_attributes):
    """Confirms that breeding levels higher than 5 are set to 5"""
    testUser = User(user_attributes["ID"],
                        user_attributes["level"],
                        datetime(2021,1,1),
                        user_attributes["warningsIssued"])
    assert testUser.breedingLevel(True) == 5

def test_breeding_level_image(user_attributes):
    """Confirms that the correct art is shown for breeding item level"""
    test_user = User(user_attributes["ID"],
                        user_attributes["level"],
                        datetime(2022,12,31),
                        user_attributes["warningsIssued"])
    assert ("https://chorumfur-bot.s3.us-east-2.amazonaws.com"\
            "/items/Breeding+Crystal5.png") == Constants.CRYSTAL_IMAGE_STAGES[test_user.breedingLevel()]

def test_update_wallet():
    wallet_before = database_methods.get_user_from_db(202632427535859712).wallet
    database_methods.update_currency_in_wallet(202632427535859712,50)
    wallet_after = database_methods.get_user_from_db(202632427535859712).wallet
    assert wallet_after == (wallet_before+50)
