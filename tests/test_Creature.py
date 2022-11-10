from src.ConstantData import Constants
from .context import Creature
from .context import Database
from datetime import datetime
import pytest

@pytest.fixture
def testCreatureAttributes():
    testCreatureAttrs = {
                            "name" : "Test Creature",
                            "owner" : 99999,
                            "ownerName" : "Test Owner",
                            "generation" : 0,
                            "creatureId" : 99999,
                            "createDate" : datetime.today(),
                            "imageLink" : "https://fakesite.com"
                        }
    return testCreatureAttrs

@pytest.fixture
def createCreature(testCreatureAttributes):
    testCreature = Creature.Creature(name=testCreatureAttributes["name"],
                                    owner = testCreatureAttributes["owner"],
                                    generation = testCreatureAttributes["generation"],
                                    creatureId = testCreatureAttributes["creatureId"],
                                    createDate=str(testCreatureAttributes["createDate"]),
                                    imageLink=testCreatureAttributes['imageLink'],
                                    ownerName=testCreatureAttributes["ownerName"])
    return testCreature

def test_createCreature(testCreatureAttributes):
    testCreature = Creature.Creature(name=testCreatureAttributes["name"],
                                    owner = testCreatureAttributes["owner"],
                                    generation = testCreatureAttributes["generation"],
                                    creatureId = testCreatureAttributes["creatureId"],
                                    createDate=str(testCreatureAttributes["createDate"])
                                    )
    assert testCreature

def test_outputCreature(createCreature,testCreatureAttributes):
    age = datetime.today() - testCreatureAttributes['createDate']
    outputString = f"""ID: {testCreatureAttributes["creatureId"]}\n"""\
                    f"""Name: {testCreatureAttributes["name"]}\n"""\
                    f"""Owner: {testCreatureAttributes["ownerName"]}\n"""\
                    f"""Age: {age}\n"""\
                    f"""Create Date: {datetime.strftime(testCreatureAttributes['createDate'],Constants.DATEONLYFORMAT)}\n"""\
                    f"""Generation: {testCreatureAttributes["generation"]}\n"""
    assert createCreature.outputCreature() == outputString

# Database Read/Write
def test_addCreatureToDB(createCreature):
    assert Database.addCreatureToDB(createCreature,test=True)

def test_getCreatureFromDB(testCreatureAttributes):
    testCreature = Database.getCreatureFromDB(1,True)
    assert testCreature.name == 'Test Creature'

def test_getCreatureFromDBThatDoesntExist(testCreatureAttributes):
    testCreature = Database.getCreatureFromDB(99999,True)
    assert not testCreature