from .context import User
import pytest
import datetime

@pytest.fixture
def userAttributes():
    userAttributes = {
                    "ID" : 99999,
                    "level" : 99,
                    "lastBreed" : datetime.datetime(2022,12,31,0,0,0,0),
                    "warningsIssued" : 0
                    }
    return userAttributes

@pytest.fixture
def createTestUser(userAttributes):
    testUser = User.User(userAttributes["ID"],
                        userAttributes["level"],
                        userAttributes["lastBreed"],
                        userAttributes["warningsIssued"])
    return testUser

def test_createUserDefault(userAttributes):
    testUser = User.User(userAttributes["ID"])
    assert testUser

def test_createUserAllValues(userAttributes):
    testUser = User.User(userAttributes["ID"],
                        userAttributes["level"],
                        userAttributes["lastBreed"],
                        userAttributes["warningsIssued"])
    assert testUser.userId == userAttributes["ID"]

def test_breedingLevel1(userAttributes):
    testUser = User.User(userAttributes["ID"],
                        userAttributes["level"],
                        datetime.datetime(2022,12,31),
                        userAttributes["warningsIssued"])
    assert testUser.breedingLevel(True) == 0

def test_breedingLevel3(userAttributes):
    testUser = User.User(userAttributes["ID"],
                        userAttributes["level"],
                        datetime.datetime(2022,12,19),
                        userAttributes["warningsIssued"])
    assert testUser.breedingLevel(True) == 2

def test_breedingLevel6(userAttributes):
    testUser = User.User(userAttributes["ID"],
                        userAttributes["level"],
                        datetime.datetime(2022,11,30),
                        userAttributes["warningsIssued"])
    assert testUser.breedingLevel(True) == 5

def test_breedingLevelUnder0(userAttributes):
    testUser = User.User(userAttributes["ID"],
                        userAttributes["level"],
                        datetime.datetime(2023,1,1),
                        userAttributes["warningsIssued"])
    assert testUser.breedingLevel(True) == 0

def test_breedingLevelAbove5(userAttributes):
    testUser = User.User(userAttributes["ID"],
                        userAttributes["level"],
                        datetime.datetime(2021,1,1),
                        userAttributes["warningsIssued"])
    assert testUser.breedingLevel(True) == 5