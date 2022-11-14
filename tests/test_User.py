from .context import User
from .context import Database
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
                    wallet=userAttributes['wallet'],
                    inventory={99:2,1:1})
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
    testUser = User(userAttributes["ID"],
                        userAttributes["level"],
                        datetime(2022,12,31),
                        userAttributes["warningsIssued"])
    assert "https://media.discordapp.net/attachments/1039966957799211109/1039967098174185552/Breeding_Crystal.png" == User.BREEDINGSTONELINKS[testUser.breedingLevel(True)]

#Mothballing This while inventory code is refactored.
"""
def test_addToInventory(createTestUser):
    createTestUser.addToInventory(99)
    assert createTestUser.inventory[99] == 3

def test_listInventory(createTestUser):
    createTestUser.inventory = {}
    createTestUser.addToInventory(99)
    createTestUser.addToInventory(99)
    createTestUser.addToInventory(1)
    
    assert createTestUser.listInventory() == "99: 2\n1: 1\n"
"""
# DB Read/Write Tests

def test_addNewUserToDB(createTestUser):
    assert Database.addUserToDB(createTestUser,True)


def test_rejectExistingUserInDB(createTestUser):
    createTestUser.userId = 99999
    assert not Database.addUserToDB(createTestUser,True)

def test_getUserFromDB():
    returnedUser = Database.getUserFromDB(99999,True)
    assertValues = (returnedUser.userId,returnedUser.level)
    assert assertValues == (99999,99)

# Mothballing these tests while code is refactored.

def test_addToUserInventory():
    assert Database.addToUserInventory(99999,800,True)

"""
def test_getInventory(createTestUser):
    createTestUser.userId = 99999
    assert Database.getInventory(createTestUser,True)
"""