"""
Data Transformation
"""

from datetime import datetime
from database import User, Region
from unidecode import unidecode


def transliterate(string):
    return unidecode(string)


def flatten_json_data(data: object):
    user_data = {
        "first_name": data.get("name", {}).get("first"),
        "last_name": data.get("name", {}).get("last"),
        "email": data["email"],
        "gender": data.get("gender"),
        "dob": data.get("dob"),
        "registration_date": data.get("registered"),
        "nationality": data.get("nat"),
    }
    region_data = {
        "city": data.get("location", {}).get("city"),
        "state": data.get("location", {}).get("state"),
    }
    return user_data, region_data


def normalize_user_data(user_data: object):
    user_data["first_name"] = (
        user_data["first_name"].capitalize()
        if user_data["first_name"] is not None
        else None
    )
    user_data["last_name"] = (
        user_data["last_name"].capitalize()
        if user_data["last_name"] is not None
        else None
    )

    # here an exception may be raised
    user_data["dob"] = datetime.strptime(user_data["dob"], "%Y-%m-%d %H:%M:%S").date()
    user_data["registration_date"] = datetime.strptime(
        user_data["registration_date"], "%Y-%m-%d %H:%M:%S"
    ).date()
    # etc
    return user_data


def normalize_region_data(region_data: object):
    region_data["city"] = (
        region_data["city"].capitalize() if region_data["city"] is not None else None
    )
    region_data["state"] = (
        region_data["state"].capitalize() if region_data["state"] is not None else None
    )
    return region_data
