"""
Data Transformation
"""

import json
from datetime import datetime

def transform_json_record(json_record):
    dob = datetime.strptime(json_record["dob"], "%Y-%m-%d %H:%M:%S").date()
    registration_date = datetime.strptime(json_record["registered"], "%Y-%m-%d %H:%M:%S").date()
    
    return {
        "first_name": json_record["name"]["first"],
        "last_name": json_record["name"]["last"],
        "email": json_record["email"],
        "gender": json_record["gender"],
        "dob": dob,
        "registration_date": registration_date,
        "nationality": json_record["nat"],
        "city": json_record["location"]["city"],
        "state": json_record["location"]["state"]
    }

def load_and_transform_json_file(filepath):
    with open(filepath, 'r') as file:
        json_data = json.load(file)
        transformed_data = transform_json_record(json_data)
        print(transformed_data)

if __name__ == "__main__":
    load_and_transform_json_file('sample.json')
