import json


def read_json_file(filename) -> list:
    res = []
    with open(filename, 'r', encoding='utf-8') as json_file:
        res = json.load(json_file)
    return res
