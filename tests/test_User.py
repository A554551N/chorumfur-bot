from .context import User
import pytest
import datetime

@pytest.fixture
def userAttributes():
    userAttributes = {
                    "ID" : 99999,
                    "level" : 1,
                    "lastBreed" : datetime.datetime.today(),
                    "warningsIssued" : 0
                    }
    return userAttributes

def test_createUserDefault(userAttributes):
    testUser = User.User(userAttributes["ID"])
    assert testUser