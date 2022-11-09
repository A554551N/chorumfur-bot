from .context import Creature
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
                    f"""Create Date: {testCreatureAttributes['createDate']}\n"""\
                    f"""Generation: {testCreatureAttributes["generation"]}\n"""\
                    f"""Image: {testCreatureAttributes['imageLink']}"""
    assert createCreature.outputCreature() == outputString