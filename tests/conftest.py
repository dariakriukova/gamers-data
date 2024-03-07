from database import Base
from sqlalchemy.orm import Session
from src.database import get_engine
import pytest
import os

TEST_DB_NAME = "test.db"


# this fixture is automatically used by all tests in the
# session without needing to be explicitly passed as a
# parameter to them. fixture is set up once at the start of
# the test session and is torn down at the end
@pytest.fixture(autouse=True, scope="session")
def set_env():
    os.environ["DB"] = TEST_DB_NAME


@pytest.fixture(scope="session")
def engine():
    try:  # clear db if it already exists to avoid issues
        os.remove(TEST_DB_NAME)
    except FileNotFoundError:
        ...
    engine = get_engine(TEST_DB_NAME)
    return engine


@pytest.fixture(scope="session")
def session(engine):
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
