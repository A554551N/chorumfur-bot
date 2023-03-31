import pytest
from datetime import datetime
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

def test_use_test_Item():
    """Tests that an Item's use effect works as intended
    
    Test passes if the return of the function is 'Item Used Successfully'
    """
    returned_messages = interface_inventory.use_item_from_inventory(99999,99)
    assert  returned_messages == 'Item Used Successfully'

def test_use_unusable_item():
    """Tests that an item that is unusable cannot be used
    Test passes if return value reads 'This Item cannot be used'
    """
    returned_messages = interface_inventory.use_item_from_inventory(99998,99)
    assert returned_messages == 'This item cannot be used'

def test_unowned_item():
    """Tests that an item not in your inventory cannot be used
    Test passes if return value reads 'Item could not be found in your inventory'
    """
    returned_messages = interface_inventory.use_item_from_inventory(99999,0)
    assert returned_messages == 'Item could not be found in your inventory'

def test_breeding_reset_item():
    """Tests that a breeding reset item successfully resets the breeding counter
    Test passes if user.lastBreed == None"""
    test_user = database_methods.get_user_from_db(99)
    test_user.lastBreed = datetime.today()
    database_methods.update_user_last_breed(test_user)
    interface_inventory.use_item_from_inventory(30,99,99)
    test_user = database_methods.get_user_from_db(99)
    assert not test_user.lastBreed

def test_give_item():
    """Tests that a user can give an item they own to another user"""
    giver_id = 99
    receiver_id = 100
    item_id = 99999
    giver_qty_before = 0
    giver_qty_after = 0
    rec_qty_before = 0
    rec_qty_after = 0
    giver_inv = database_methods.get_user_inventory(99)
    for row in giver_inv:
        if row[0] == 99999:
            giver_qty_before = row[2]
    receiver_inv = database_methods.get_user_inventory(100)
    for row in receiver_inv:
        if row[0] == 99999:
            rec_qty_before = row[2]
    interface_inventory.give_item(giver_id,receiver_id,item_id,1)
    giver_inv = database_methods.get_user_inventory(99)
    for row in giver_inv:
        if row[0] == 99999:
            giver_qty_after = row[2]
    receiver_inv = database_methods.get_user_inventory(100)
    for row in receiver_inv:
        if row[0] == 99999:
            rec_qty_after = row[2]
    assert (giver_qty_before-1 == giver_qty_after),(rec_qty_before+1 == rec_qty_after)

def test_cant_give_unowned_item():
    """Tests to confirm that a user can't give away items they don't own"""
    assert interface_inventory.give_item(99,100,10000,1) == "Items could not be transferred."

def test_cant_give_too_many_items():
    """Tests that a user can't give more of an item away than they have"""
    assert interface_inventory.give_item(99,100,99999,10000000) == "Items could not be transferred."
