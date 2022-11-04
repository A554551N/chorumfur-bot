from .context import Creature
import time
import pytest

@pytest.fixture
def testCreatureAttributes():
    rawDate = time.localtime()
    formattedDate = [rawDate.tm_year,rawDate.tm_mon,rawDate.tm_mday]
    testCreatureAttrs = {
                            "name" : "Test Creature",
                            "owner" : 99999,
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
                                    generation = testCreatureAttributes["generation"],
                                    creatureId = testCreatureAttributes["creatureId"],
                                    date=testCreatureAttributes["date"],
                                    isNew=True)
    return testCreature

def test_createCreature(testCreatureAttributes):
    testCreature = Creature.Creature(name=testCreatureAttributes["name"],
                                    owner = testCreatureAttributes["owner"],
                                    generation = testCreatureAttributes["generation"],
                                    creatureId = testCreatureAttributes["creatureId"],
                                    date=testCreatureAttributes["date"],
                                    isNew=True)
    assert testCreature

def test_createDate(createCreature,testCreatureAttributes):
    """Tests that createDate is being formatted properly before storage"""
    assert createCreature.createDate == testCreatureAttributes["fdate"]

def test_outputCreature(createCreature,testCreatureAttributes):
    outputString = f"""ID: {testCreatureAttributes["creatureId"]}\n"""\
                    f"""Name: {testCreatureAttributes["name"]}\n"""\
                    f"""Owner: {testCreatureAttributes["owner"]}\n"""\
                    f"""Create Date: {testCreatureAttributes["fdate"][1]} {testCreatureAttributes["fdate"][2]} {testCreatureAttributes["fdate"][0]}\n"""\
                    f"""Generation: {testCreatureAttributes["generation"]}"""    
    assert createCreature.outputCreature() == outputString