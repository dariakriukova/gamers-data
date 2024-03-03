from src.database import setup_db, User
import pytest
from sqlalchemy.orm import Session

class TestLoad:
    
    
    def test_it_works(self, engine):
        with Session(engine) as session:
            assert session.query(User).count() == 0
