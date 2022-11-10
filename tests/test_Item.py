import pytest
from .context import Item

@pytest.fixture
def testItemAttributes():
    testItemAttrs = {
        'name' : 'Test Item',
        'description' : 'Test Item Description',
        'imageLink' : 'http://www.fakesite.com',
        'value' : 9999,
        'id' : 1
    }

    return testItemAttrs

def test_createItem(testItemAttributes):
    testItem = Item.Item(testItemAttributes['name'],
                        testItemAttributes['description'],
                        testItemAttributes['value'],
                        testItemAttributes['imageLink'],
                        testItemAttributes['id'])

    assert testItem