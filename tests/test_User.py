from .context import User
from .context import database_methods
from .context import Item
import random
import pytest
from datetime import datetime

@pytest.fixture
def userAttributes():
    userAttributes = {
                    "ID" : random.randint(1,1000000),
                    "level" : 99,
                    "wallet" : 0,
                    "lastBreed" : datetime(2022,12,31),
                    "warningsIssued" : 0
                    }
    return userAttributes

@pytest.fixture
def createTestUser(userAttributes):
    testUser = User(userId=userAttributes["ID"],
                    level=userAttributes["level"],
                    lastBreed=userAttributes["lastBreed"],
                    warningsIssued=userAttributes["warningsIssued"],
                    wallet=userAttributes['wallet'])
    return testUser

def test_createUserDefault(userAttributes):
    testUser = User(userAttributes["ID"])
    assert testUser

def test_createUserAllValues(userAttributes):
    testUser = User(userAttributes["ID"],
                        userAttributes["level"],
                        userAttributes["lastBreed"],
                        userAttributes["warningsIssued"])
    assert testUser.userId == userAttributes["ID"]

def test_breedingLevel1(userAttributes):
    testUser = User(userAttributes["ID"],
                        userAttributes["level"],
                        datetime(2022,12,31),
                        userAttributes["warningsIssued"])
    assert testUser.breedingLevel(True) == 0

def test_breedingLevel3(userAttributes):
    testUser = User(userAttributes["ID"],
                        userAttributes["level"],
                        datetime(2022,12,19),
                        userAttributes["warningsIssued"])
    assert testUser.breedingLevel(True) == 2

def test_breedingLevel6(userAttributes):
    testUser = User(userAttributes["ID"],
                        userAttributes["level"],
                        datetime(2022,11,30),
                        userAttributes["warningsIssued"])
    assert testUser.breedingLevel(True) == 5

def test_breedingLevelUnder0(userAttributes):
    testUser = User(userAttributes["ID"],
                        userAttributes["level"],
                        datetime(2023,1,1),
                        userAttributes["warningsIssued"])
    assert testUser.breedingLevel(True) == 0

def test_breedingLevelAbove5(userAttributes):
    testUser = User(userAttributes["ID"],
                        userAttributes["level"],
                        datetime(2021,1,1),
                        userAttributes["warningsIssued"])
    assert testUser.breedingLevel(True) == 5

def test_breedingLevelImage(userAttributes):
    """Confirms that the correct art is shown for breeding item level"""
    testUser = User(userAttributes["ID"],
                        userAttributes["level"],
                        datetime(2022,12,31),
                        userAttributes["warningsIssued"])
    assert "https://media.discordapp.net/attachments/1039966957799211109/1039967098174185552/Breeding_Crystal.png" == User.BREEDINGSTONELINKS[testUser.breedingLevel(True)]

# DB Read/Write Tests

def test_add_new_user_to_db(userAttributes):
    """Attempts to add a user to the database and asserts that it completed successfully"""
    assert database_methods.add_user_to_database(userAttributes["ID"])


def test_reject_existing_user_in_db(createTestUser):
    """Asserts that duplicate users are not added to database"""
    createTestUser.userId = 99999
    assert not database_methods.add_user_to_database(createTestUser.userId)

def test_get_user_from_db():
    """asserts that a user can be retreived from the database"""
    returnedUser = database_methods.get_user_from_db(99999)
    assertValues = (returnedUser.userId,returnedUser.level)
    assert assertValues == (99999,99)

# Mothballing these tests while code is refactored.

def test_addToUserInventory():
    assert Database.addToUserInventory(99999,800,True)

def test_getInventory(createTestUser):
    createTestUser.userId = 99998
    testUser = Database.getUserInventory(createTestUser,True)
    assert testUser.inventory[1][1] == 2

def test_emptyInventoryReturnsNone(createTestUser):
    createTestUser.userId = 123
    testUser = Database.getUserInventory(createTestUser,True)
    assert not testUser.inventory

def test_removeItemFromInventory(createTestUser):
    createTestUser.userId = 99999
    Database.addToUserInventory(99999,1000,True)
    Database.removeFromUserInventory(99999,1000,True)
    testUser = Database.getUserInventory(createTestUser,True)
    assert 1000 not in testUser.inventory.keys()