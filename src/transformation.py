"""
Data Transformation
"""

from datetime import datetime
from database import User, Region

def flatten_json_data(data):
    user_data = {
        "first_name": data["name"]["first"],
        "last_name": data["name"]["last"],
        "email": data["email"],
        "gender": data["gender"],
        "dob": datetime.strptime(data["dob"], "%Y-%m-%d %H:%M:%S").date(),
        "registration_date": datetime.strptime(data["registered"], "%Y-%m-%d %H:%M:%S").date(),
        "nationality": data["nat"],
    }
    region_data = {
        "city": data["location"]["city"],
        "state": data["location"]["state"],
        }
    user =  User(**user_data)
    user.region = Region(**region_data)
    return user


