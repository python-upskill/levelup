import re
from util import json_operations
from random import randint

class DiceSimulator:
    def encode(self, expr: str):
        prefix_pattern = '(\d+)d(\d+)'
        suffix_pattern = '\s+\+\s+(\d+)'
        pattern = prefix_pattern + suffix_pattern
        x = 0
        y = 0
        z = 0
        if (re.match(pattern, expr)):
            z = int(re.search(pattern, expr).group(3))
        pattern = prefix_pattern
        if (re.match(pattern, expr)):
            x = re.search(pattern, expr).group(1)
            y = re.search(pattern, expr).group(2)
        self.__init(int(x), int(y), int(z))
        return self

    def __init(self, x: int, y: int, z: int):
        self.x = x
        self.y = y
        self.z = z

    def random_result(self):
        sum = 0
        for _ in range(self.x):
            sum += randint(1, self.y)
        sum += self.z
        return sum


class Combatant(object):
    def __init__(self, name: str, hp: int, damage: str):
        self.name = name
        self.hp = hp
        self.damage = DiceSimulator().encode(damage).random_result()


def create_combatants(path):
    elements = json_operations.read_from_file(path)
    result = []
    for e in elements:
        result.append(Combatant(**e))
    return result


print(create_combatants('../tasks/combat/combatants.json')[0].damage)