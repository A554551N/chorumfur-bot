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
    assert not test_ticket.requestor_can_breed()

def test_cannot_breed_when_crystal_empty():
    """Test should reject user attempt to breed without a full crystal."""
    creature_a = Creature("Test_A",111)
    creature_b = Creature("Test_A",111)
    test_user = User(111,lastBreed=datetime.today())
    test_ticket = Ticket('Test Ticket',test_user,creature_a,creature_b)
    assert not test_ticket.requestor_can_breed()

def test_can_breed_when_owning_one():
    """Test should return True when user attempts to breed creature they own one of"""
    creature_a = Creature("Test_A",111)
    creature_b = Creature("Test_A",222)
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

def test_get_ticket_from_db():
    """Test should retreive a ticket from the database and return its ID"""
    test_ticket = database_methods.get_ticket_from_db(1)
    expected_result = (1,27,28,202632427535859712)
    returned_value = (
        test_ticket.id,
        test_ticket.creature_a.creatureId,
        test_ticket.creature_b.creatureId,
        test_ticket.requestor.userId)
    assert expected_result == returned_value

