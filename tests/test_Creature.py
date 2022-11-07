from .context import Creature
import time
import pytest

@pytest.fixture
def testCreatureAttributes():
    testCreatureAttrs = {
                            "name" : "Test Creature",
                            "owner" : 99999,
                            "generation" : 0,
                            "creatureId" : 99999,
                            "createDate" : time.localtime()
                        }
    return testCreatureAttrs

@pytest.fixture
def createCreature(testCreatureAttributes):
    testCreature = Creature.Creature(name=testCreatureAttributes["name"],
                                    owner = testCreatureAttributes["owner"],
                                    generation = testCreatureAttributes["generation"],
                                    creatureId = testCreatureAttributes["creatureId"],
                                    createDate=testCreatureAttributes["createDate"])
    return testCreature

def test_createCreature(testCreatureAttributes):
    testCreature = Creature.Creature(name=testCreatureAttributes["name"],
                                    owner = testCreatureAttributes["owner"],
                                    generation = testCreatureAttributes["generation"],
                                    creatureId = testCreatureAttributes["creatureId"],
                                    createDate=testCreatureAttributes["createDate"])
    assert testCreature

def test_createDate(createCreature,testCreatureAttributes):
    """Tests that createDate is being formatted properly before storage"""
    assert createCreature.createDate == testCreatureAttributes["createDate"]

def test_outputCreature(createCreature,testCreatureAttributes):
    outputString = f"""ID: {testCreatureAttributes["creatureId"]}\n"""\
                    f"""Name: {testCreatureAttributes["name"]}\n"""\
                    f"""Owner: {testCreatureAttributes["owner"]}\n"""\
                    f"""Create Date: {testCreatureAttributes['createDate']}\n"""\
                    f"""Generation: {testCreatureAttributes["generation"]}"""    
    assert createCreature.outputCreature() == outputString