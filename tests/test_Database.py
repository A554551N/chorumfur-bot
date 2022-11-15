import pytest
from datetime import datetime
import random
from .context import Database

def test_database_connection_prod():
    conn = Database.create_connection()
    assert conn
    conn.close()

def test_database_connection_nonprod():
    conn = Database.create_connection(test=True)
    assert conn

    conn.close()
    
"""
#User DB Tests
def test_addNewUserToDB(createUser):
    assert Database.addUserToDB(createUser,True)

def test_rejectExistingUserInDB(createUser):
    createUser.userId = 99999
    assert not Database.addUserToDB(createUser,True)

def test_getUserFromDB():
    returnedUser = Database.getUserFromDB(99999,True)
    assertValues = (returnedUser.userId,returnedUser.level)
    assert assertValues == (99999,99)

def test_updateLastBreed(createUser):
    lastBreed = datetime(2021,1,1)
    createUser.userId = 99999
    createUser.updateLastBreed(lastBreed)
    returnedUser = Database.getUserFromDB(createUser.userId)
    assert createUser.lastBreed == lastBreed
"""