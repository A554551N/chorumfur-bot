import pytest
import datetime
from .context import Database
from .context import Creature

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

def test_getCreatureFromDB(testCreatureAttributes):
    testCreature = Database.getCreatureFromDB(1,True)
    assert testCreature.name == 'Test Creature'

def test_getCreatureFromDBThatDoesntExist(testCreatureAttributes):
    testCreature = Database.getCreatureFromDB(99999,True)
    assert not testCreature