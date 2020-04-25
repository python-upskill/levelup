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
        return sum + self.z


class Combatant(object):
    def __init__(self, name: str, hp: int, damage: str):
        self.name = name
        self.hp_before_attach = hp
        self.hp_after_attack = hp
        self.damage_pattern = damage

    def __random_damage(self):
        return DiceSimulator().encode(self.damage_pattern).random_result()

    def attack(self, other: 'Combatant'):
        other.hp_before_attach = other.hp_after_attack
        self.opponent = other
        other.opponent = self
        self.damage = self.__random_damage()
        other.hp_after_attack -= self.damage

    def is_won(self):
        return hasattr(self, 'opponent') and self.opponent.hp_after_attack <= 0

    def print_round(self, round_number: int):
        print('{} {} {} {} {} {}'.format(round_number, self.name, self.opponent.name, self.damage,
                                         self.opponent.hp_before_attach, self.opponent.hp_after_attack))


def create_combatants(path = '../tasks/combat/combatants.json'):
    elements = json_operations.read_from_file(path)
    result = []
    for e in elements:
        result.append(Combatant(**e))
    return result


# print(create_combatants('../tasks/combat/combatants.json')[0].random_damage())
# print(create_combatants('../tasks/combat/combatants.json')[0])
# print(create_combatants()[0])

# combatants = create_combatants()
# c1 = combatants[0]
# c2 = combatants[1]
# c1.attack(c2)
# c1.print_round(1)
# c1.attack(c2)
# c1.print_round(2)
#
# print('{} - {}'.format(1, 'a'))