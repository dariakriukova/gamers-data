"""
Data Transformation
"""

from datetime import datetime
from unidecode import unidecode



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

def normalize_user_data(user_data: dict):
    keys_to_normalize = ["first_name", "last_name", "gender", "nationality"]
    
    for key in keys_to_normalize:
        if user_data.get(key) is not None:
            transliterated_text = unidecode(user_data[key])
            lower_case_text = transliterated_text.lower()
            cleaned_text = lower_case_text.replace('-', ' ')
            user_data[key] = cleaned_text

    # here an exception may be raised
    user_data["dob"] = datetime.strptime(user_data["dob"], "%Y-%m-%d %H:%M:%S").date()
    user_data["registration_date"] = datetime.strptime(
        user_data["registration_date"], "%Y-%m-%d %H:%M:%S"
    ).date()
    return user_data


def normalize_region_data(region_data: dict):
    keys_to_normalize = ["city", "state"]
    
    for key in keys_to_normalize:
        if region_data.get(key) is not None:
            transliterated_text = unidecode(region_data[key])
            lower_case_text = transliterated_text.lower()
            cleaned_text = lower_case_text.replace('-', ' ')
            region_data[key] = cleaned_text

    return region_data

