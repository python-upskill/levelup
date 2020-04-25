import re
from util import json_operations
from random import randint

WORKS = True


class DiceSimulator:
    def __init__(self): pass

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
    # def __init__(self): pass
    def __init__(self, name: str, hp: int, damage: str):
        self.name = name
        self.hp = hp
        self.damage = DiceSimulator().encode(damage).random_result()

    def ss(self, s):
        return "X" + s + "X"


# class Combatant
def create_combatants(path):
    elements = json_operations.read_from_file(path)
    result = []
    for e in elements:
        result.append(Combatant(**e))
    return result
    # def __init__(self, file_path: str):
    #     self(json_operations.read_from_file(file_path))
    # def init(self, name: str, hp: int, damage: str):
    #     self.name = name
    #     self.hp = hp
    #     self.damage = damage

    # def init(self, path: str):
    #     pass


# print(json_operations.read_from_file('../tasks/combat/combatants.json'))

# print('===== ' + Combatant('../tasks/combat/combatants.json').damage)
# Combatant('../tasks/combat/combatants.json')

# r = json_operations.read_from_file('../tasks/combat/combatants.json')
# print(str(r[0]))
# # d= Combatant(**r[0])
# d= Combatant()
# d.init(**json_operations.read_from_file('../tasks/combat/combatants.json')[0])
# print(d.name)

print(create_combatants('../tasks/combat/combatants.json')[0].damage)

txt = "3d10+9"
prefix_pattern = '(\d+)d(\d+)'
suffix_pattern = '\s*\+\s*(\d+)'
pattern = prefix_pattern + suffix_pattern
print('### ' + re.search(pattern, txt).group(3))
if re.match(pattern, txt):
    print('a')
else:
    print('b')
