from src.database import setup_db
import pytest
import os
   
TEST_DB_NAME = 'test.db'

@pytest.fixture()
def engine():
    engine = setup_db(TEST_DB_NAME)
    return engine

@pytest.fixture(autouse=True)
def set_env():
    os.environ['DB'] = TEST_DB_NAME