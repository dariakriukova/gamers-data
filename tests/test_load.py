from pathlib import Path
from src.database import User
from src.load import read_json_lines, read_csv_lines
import pytest
from sqlalchemy.orm import Session


class TestReadJsonLines:
    @pytest.fixture()
    def huge_json_file(self):
        return Path('tests/data/huge.json')
    
    @pytest.fixture()
    def corrupted_json_file(self):
        return Path('tests/data/corrupted.json')
    
    def test_parse_huge_file(self, huge_json_file):
        users_data, regions_data = read_json_lines(huge_json_file)
        assert len(users_data) == 1000
        assert len(regions_data) == 1000
    
    def test_parse_corrupted_file(self, corrupted_json_file):
        users_data, regions_data = read_json_lines(corrupted_json_file)
        assert len(users_data) == 6
        assert len(regions_data) == 6

class TestReadCsvLines:
    @pytest.fixture()
    def huge_csv_file(self):
        return Path('tests/data/huge.csv')
    
    @pytest.fixture()
    def corrupted_csv_file(self):
        return Path('tests/data/corrupted.csv')
    
    def test_parse_huge_file(self, huge_csv_file):
        users_data = read_csv_lines(huge_csv_file)
        assert len(users_data) == 1000
        
    def test_parse_corrupted_file(self, corrupted_csv_file):
        users_data = read_csv_lines(corrupted_csv_file)
        assert len(users_data) == 10
        

class TestLoad:
    # TODO
    def test_it_works(self, engine):
        with Session(engine) as session:
            assert session.query(User).count() == 0
