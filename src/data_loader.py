"""
Data loader
"""

import json

data_28 = load_json("28/wwc.json")
data_29 = load_json("29/wwc.json")


def read_json_lines(file_path):
    data_list = []
    with open(file_path, 'r') as file:
        for line in file:
            json_data = json.loads(line)
            data_list.append(json_data)
    return data_list


data = read_json_lines('data/wwc/2021/04/29/wwc.json')

