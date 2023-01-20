from src.ConstantData import Constants
from .context import Creature
from .context import database_methods
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
    test_creature = Creature(name=testCreatureAttributes["name"],
                            owner = testCreatureAttributes["owner"],
                            generation = testCreatureAttributes["generation"],
                            creatureId = testCreatureAttributes["creatureId"],
                            createDate=str(testCreatureAttributes["createDate"]),
                            imageLink=testCreatureAttributes['imageLink'],
                            ownerName=testCreatureAttributes["ownerName"])
    return test_creature

def test_createCreature(testCreatureAttributes):
    testCreature = Creature(name=testCreatureAttributes["name"],
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

def test_randomize_creature(createCreature):
    """Tests the randomize creature function to confirm all traits are generated."""
    createCreature.randomize_creature()
    assertion = True
    for value in createCreature.traits.values():
        if not value:
            assertion = False
    assert assertion

# Database Read/Write
def test_add_creature_to_db(createCreature):
    assert database_methods.add_creature_to_db(createCreature)

def test_get_creature_from_db(testCreatureAttributes):
    test_creature = database_methods.get_creature_from_db(28)
    assert test_creature.name == 'Test Creature'

def test_get_creature_from_db_that_doesnt_exist(testCreatureAttributes):
    testCreature = database_methods.get_creature_from_db(99999)
    assert not testCreature