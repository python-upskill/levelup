import json


def read_from_file(path):
    with open(path) as f:
        return json.load(f)