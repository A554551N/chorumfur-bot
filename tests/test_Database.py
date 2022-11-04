import pytest
import os
from .context import Database

def test_database_connection():
    conn = Database.create_connection(os.path.join(os.path.dirname(__file__), '../database.db'))
    assert conn
    conn.close()