from src.transformation import (
    flatten_json_data,
    parse_date,
    normalize_string,
)
import pytest
from datetime import date


class TestFlattenJsonData:
    @pytest.mark.parametrize(
        "input_data,expected_user_data,expected_region_data",
        [
            (
                {
                    "name": {"first": "John", "last": "Doe"},
                    "email": "johndoe@example.com",
                    "gender": "male",
                    "dob": "1990-01-01",
                    "registered": "2010-01-01",
                    "nat": "US",
                    "location": {"city": "New York", "state": "New York"},
                },
                {
                    "first_name": "John",
                    "last_name": "Doe",
                    "email": "johndoe@example.com",
                    "gender": "male",
                    "dob": "1990-01-01",
                    "registration_date": "2010-01-01",
                    "nationality": "US",
                },
                {"city": "New York", "state": "New York"},
            ),
            (
                {
                    "name": {"last": "Doe"},
                    "email": "johndoe@example.com",
                    "gender": "male",
                    "registered": "2010-01-01",
                    "location": {"city": "New York", "state": "New York"},
                },
                {
                    "first_name": None,
                    "last_name": "Doe",
                    "email": "johndoe@example.com",
                    "gender": "male",
                    "dob": None,
                    "registration_date": "2010-01-01",
                    "nationality": None,
                },
                {"city": "New York", "state": "New York"},
            ),
            (
                {
                    "name": {"last": "Doe"},
                    "email": "johndoe@example.com",
                    "gender": "male",
                    "registered": "2010-01-01",
                    "some_extra_property": 1234,
                },
                {
                    "first_name": None,
                    "last_name": "Doe",
                    "email": "johndoe@example.com",
                    "gender": "male",
                    "dob": None,
                    "registration_date": "2010-01-01",
                    "nationality": None,
                },
                {"city": None, "state": None},
            ),
        ],
    )
    def test_flatten_json_data_returns_user_and_region_data(
        self, input_data, expected_user_data, expected_region_data
    ):
        user_data, region_data = flatten_json_data(input_data)
        assert user_data == expected_user_data
        assert region_data == expected_region_data


class TestNormalizeString:
    @pytest.mark.parametrize(
        "input,expected",
        [
            ("Hello WORLD$!", "hello world"),
            ("1234", ""),
            ("John_Doe-2024!", "john doe"),
            ("Äëïó üñîçødé", "aeio unicode"),
            ("  multiple   spaces   ", "multiple spaces"),
            ("special#$%^&*()chars", "special chars"),
        ],
    )
    def test_normalize_string_normalizes(self, input, expected):
        assert normalize_string(input) == expected

    @pytest.mark.parametrize(
        "input,expected",
        [
            (None, None),
            (1234, 1234),
        ],
    )
    def test_normalize_string_ignores_non_strings(self, input, expected):
        assert normalize_string(input) == expected


class TestNormilizeDate:
    @pytest.mark.parametrize(
        "input,expected",
        [
            ("2023-01-01 00:00:00", date(2023, 1, 1)),
            ("12/31/2023", date(2023, 12, 31)),
            ("01/01/2023", date(2023, 1, 1)),
            ("", None),
            (None, None),
            ("invalid-date", None),
            ("29/02/2024", None),
        ],
    )
    def test_normalize_date(self, input, expected):
        assert parse_date(input) == expected
