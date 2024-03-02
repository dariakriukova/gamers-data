"""
Data Transformation
"""

from datetime import datetime
import re
from unidecode import unidecode



def flatten_json_data(data: dict):
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


def normalize_string(raw_data):
    if isinstance(raw_data, str):
        transliterated_text = unidecode(raw_data)
        lower_case_text = transliterated_text.lower()
        cleaned_text = re.sub(r'[^a-z]', ' ', lower_case_text)
        cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
        return cleaned_text.strip()
    else:
        return raw_data

def normalize_date(raw_data):
    if raw_data is None:
        return None
    
    patterns = ["%Y-%m-%d %H:%M:%S", "%m/%d/%Y"]
    for pat in patterns:
        try:
            return datetime.strptime(raw_data, pat).date()
        except ValueError:
            ...
    return None
    

def normalize_user_data(user_data: dict):
    keys_to_normalize = ["first_name", "last_name", "gender", "nationality"]
    for key in keys_to_normalize:
        user_data[key] = normalize_string(user_data.get(key))

    # here an exception may be raised
    user_data["dob"] = normalize_date(user_data.get("dob"))
    user_data["registration_date"] = normalize_date(user_data.get("registration_date"))
    return user_data


def normalize_region_data(region_data: dict):
    keys_to_normalize = ["city", "state"]
    for key in keys_to_normalize:
        region_data[key] = normalize_string(region_data[key])

    return region_data

