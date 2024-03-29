from datetime import datetime
import pytest
from .context import database_methods
from .context import Ticket
from .context import User
from .context import Creature

def test_cannot_breed_unowned_creatures():
    """Test should reject user attempt to breed creatures they do not own."""
    creature_a = Creature("Test_A",111)
    creature_b = Creature("Test_A",111)
    test_user = User(222,lastBreed=datetime(2022,1,1))
    test_ticket = Ticket('Test Ticket',test_user,creature_a,creature_b)
    assert not test_ticket.requestor_can_breed()[0]

def test_cannot_breed_when_crystal_empty():
    """Test should reject user attempt to breed without a full crystal."""
    creature_a = Creature("Test_A",111)
    creature_b = Creature("Test_A",111)
    test_user = User(111,lastBreed=datetime.today())
    test_ticket = Ticket('Test Ticket',test_user,creature_a,creature_b)
    assert not test_ticket.requestor_can_breed()[0]

def test_can_breed_when_owning_one():
    """Test should return True when user attempts to breed creature they own one of"""
    creature_a = Creature("Test_A",111,creatureId=1)
    creature_b = Creature("Test_A",222,creatureId=2)
    test_user = User(111,lastBreed=datetime(2022,1,1))
    test_ticket = Ticket('Test Ticket',test_user,creature_a,creature_b)
    assert test_ticket.requestor_can_breed()

def test_owns_both_creatures():
    creature_a = Creature("Test_A",111)
    creature_b = Creature("Test_A",111)
    test_user = User(111,lastBreed=datetime(2022,1,1))
    test_ticket = Ticket('Test Ticket',test_user,creature_a,creature_b)
    assert test_ticket.requestor_owns_both()

def test_add_ticket_to_db():
    """Test should add a ticket to the database and return its ID."""
    creature_a = database_methods.get_creature_from_db(27)
    creature_b = database_methods.get_creature_from_db(28)
    user = database_methods.get_user_from_db(202632427535859712)
    user.lastBreed = datetime(2022,1,1)
    test_ticket = Ticket("Test Ticket",user,creature_a,creature_b)
    assert database_methods.add_ticket_to_db(test_ticket)

def test_add_mod_ticket_to_db():
    """Test to add a modification ticket to DB"""
    creature_a = database_methods.get_creature_from_db(27)
    ticket_type = 'modification'
    user = database_methods.get_user_from_db(202632427535859712)
    user.lastBreed = datetime(2022,1,1)
    test_ticket = Ticket("Test Ticket",user,creature_a,None,ticket_type=ticket_type)
    assert database_methods.add_ticket_to_db(test_ticket)

def test_get_ticket_from_db():
    """Test should retreive a ticket from the database and return its ID"""
    test_ticket = database_methods.get_ticket_from_db(139)
    assert test_ticket.id

def test_update_ticket_status():
    """Test should update a ticket status, and then retreive it to confirm update."""
    creature_a = database_methods.get_creature_from_db(167)
    creature_b = database_methods.get_creature_from_db(168)
    user = database_methods.get_user_from_db(202632427535859712)
    user.lastBreed = datetime(2022,1,1)
    test_ticket = Ticket("Test Ticket",user,creature_a,creature_b)
    test_ticket.id = database_methods.add_ticket_to_db(test_ticket)
    test_ticket.update_ticket_status(4)
    database_methods.update_ticket_status(test_ticket)
    returned_ticket = database_methods.get_ticket_from_db(test_ticket.id)
    assert returned_ticket.status == 'Ticket in Progress'

