"""
Data Transformation
"""

from datetime import datetime
from database import User, Region

def capitalize_first_letter(string):
    if string:
        return string.capitalize()
    return string

def flatten_json_data(data):
    first_name = data.get("name", {}).get("first", "Unknown")
    last_name = data.get("name", {}).get("last", "Unknown")
    
    user_data = {
        "first_name": capitalize_first_letter(first_name),
        "last_name": capitalize_first_letter(last_name),
        "email": data["email"],
        "gender": data.get("gender", "Not specified"),
        "dob": datetime.strptime(data.get("dob", "1900-01-01 00:00:00"), "%Y-%m-%d %H:%M:%S").date(),
        "registration_date": datetime.strptime(data.get("registered", "1900-01-01 00:00:00"), "%Y-%m-%d %H:%M:%S").date(),
        "nationality": data.get("nat", "Unknown"),
    }
    region_data = {
        "city": capitalize_first_letter(data.get("location", {}).get("city")),
        "state": capitalize_first_letter(data.get("location", {}).get("state")),
        }
    
    user =  User(**user_data)
    user.region = Region(**region_data)
    return user


