import pytest
from .context import database_methods
from .context import Item
from .context import interface_inventory

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

def test_create_item(testItemAttributes):
    """Tests that an item is successfully created"""
    testItem = Item(testItemAttributes['name'],
                        testItemAttributes['description'],
                        testItemAttributes['value'],
                        testItemAttributes['imageLink'],
                        testItemAttributes['id'])

    assert testItem

def test_add_item_to_type_db(testItemAttributes):
    """Tests that a new Item type can be successfully added to the database."""
    test_item = Item(testItemAttributes['name'],
                        testItemAttributes['description'],
                        testItemAttributes['value'],
                        testItemAttributes['imageLink'])
    assert database_methods.add_item_to_db(test_item)

def test_get_item_from_type_db(testItemAttributes):
    """Retreives an item from the type database"""
    received_item = database_methods.get_item_from_db(1)
    assert_pair = (received_item.id,received_item.name)
    assert assert_pair == (1,'Beach Fun')

def test_getAllItemsInDB():
    """Tests that all items are retreived from database"""
    result = database_methods.get_all_items_from_db()
    assert result

def test_get_inventory():
    """Tests that .inventory is working as expected.  Test assumes that requesting
    user is ID 99
    
    Test passes if returned inventory is not empty."""

    inventory_message = interface_inventory.get_inventory(99)
    assert inventory_message != "No Items Found"
