import pytest
import os
import time
from .context import Database
from .context import Creature

@pytest.fixture
def testCreatureAttributes():
    rawDate = time.localtime()
    formattedDate = [rawDate.tm_year,rawDate.tm_mon,rawDate.tm_mday]
    testCreatureAttrs = {
                            "name" : "Test Creature",
                            "owner" : 99999,
                            "imageLink" : "",
                            "generation" : 0,
                            "creatureId" : 99999,
                            "date" : rawDate,
                            "fdate" : formattedDate
                        }
    return testCreatureAttrs

@pytest.fixture
def createCreature(testCreatureAttributes):
    testCreature = Creature.Creature(name=testCreatureAttributes["name"],
                                    owner = testCreatureAttributes["owner"],
                                    imageLink = testCreatureAttributes["imageLink"],
                                    generation = testCreatureAttributes["generation"],
                                    creatureId = testCreatureAttributes["creatureId"],
                                    date=testCreatureAttributes["date"],
                                    isNew=True)
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
    assert testCreature[0][1] == 'Test Creature'