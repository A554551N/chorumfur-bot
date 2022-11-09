import pytest
import datetime
import random
from .context import Database
from .context import Creature
from .context import User

@pytest.fixture
def testCreatureAttributes():
    testCreatureAttrs = {
                            "name" : "Test Creature",
                            "owner" : 99999,
                            "imageLink" : "",
                            "generation" : 0,
                            "creatureId" : 99999,
                            "createDate" : datetime.datetime.today()
                        }
    return testCreatureAttrs

@pytest.fixture
def createCreature(testCreatureAttributes):
    testCreature = Creature.Creature(name=testCreatureAttributes["name"],
                                    owner = testCreatureAttributes["owner"],
                                    imageLink = testCreatureAttributes["imageLink"],
                                    generation = testCreatureAttributes["generation"],
                                    creatureId = testCreatureAttributes["creatureId"],
                                    createDate=str(testCreatureAttributes["createDate"])
                                    )
    return testCreature

@pytest.fixture
def testUserAttributes():
    testUserAttributes = {
        "userId" : random.randint(1,1000000),
        "level" : 99,
        "lastBreed" : datetime.datetime(2022,12,31),
        "warningsIssued" : 0
    }
    return testUserAttributes

@pytest.fixture
def createUser(testUserAttributes):
    testUser = User.User(
        testUserAttributes["userId"],
        testUserAttributes["level"],
        testUserAttributes["lastBreed"],
        testUserAttributes["warningsIssued"]
    )
    return testUser

def test_database_connection_prod():
    conn = Database.create_connection()
    assert conn
    conn.close()

def test_database_connection_nonprod():
    conn = Database.create_connection(test=True)
    assert conn

    conn.close()
def test_addCreatureToDB(createCreature):
    assert Database.addCreatureToDB(createCreature,test=True)

# Creature DB tests
def test_getCreatureFromDB(testCreatureAttributes):
    testCreature = Database.getCreatureFromDB(1,True)
    assert testCreature.name == 'Test Creature'

def test_getCreatureFromDBThatDoesntExist(testCreatureAttributes):
    testCreature = Database.getCreatureFromDB(99999,True)
    assert not testCreature

#User DB Tests
def test_addNewUserToDB(createUser):
    assert Database.addUserToDB(createUser,True)

def test_rejectExistingUserInDB(createUser):
    createUser.userId = 99999
    assert not Database.addUserToDB(createUser,True)

def test_getUserFromDB():
    returnedUser = Database.getUserFromDB(99999,True)
    assertValues = (returnedUser.userId,returnedUser.level)
    assert assertValues == (99999,99)

"""
def test_updateLastBreed(createUser):
    lastBreed = datetime.datetime(2021,1,1)
    createUser.userId = 99999
    createUser.updateLastBreed(lastBreed)
    returnedUser = Database.getUserFromDB(createUser.userId)
    assert createUser.lastBreed == lastBreed
"""