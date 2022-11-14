import pytest
from .context import Database
from .context import Item

@pytest.fixture
def testItemAttributes():
    testItemAttrs = {
        'name' : "Test Item",
        'description' : "Test Item Description",
        'imageLink' : "http://www.fakesite.com",
        'value' : 9999,
        'id' : 1
    }

    return testItemAttrs

def test_createItem(testItemAttributes):
    testItem = Item(testItemAttributes['name'],
                        testItemAttributes['description'],
                        testItemAttributes['value'],
                        testItemAttributes['imageLink'],
                        testItemAttributes['id'])

    assert testItem

def test_addItemToTypeDB(testItemAttributes):
    testItem = Item(testItemAttributes['name'],
                        testItemAttributes['description'],
                        testItemAttributes['value'],
                        testItemAttributes['imageLink'])
    assert Database.addItemToDB(testItem,True)

def test_getItemFromTypeDB(testItemAttributes):
    receivedItem = Database.getItemFromDB(testItemAttributes['id'],True)
    assertPair = (receivedItem.id,receivedItem.name)
    assert assertPair == (testItemAttributes['id'],testItemAttributes['name'])

def test_getAllItemsInDB():
    result = Database.getAllItemsInDB(True)
    assert result