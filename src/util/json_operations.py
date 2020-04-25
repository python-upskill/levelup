import json

def read_from_file(path):
    with open(path) as f:
        return json.load(f)

# print(read_from_file('../../tasks/combat/combatants.json'))