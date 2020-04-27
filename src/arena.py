import json
import re
import random
from typing import List


class Damage:
    __x: int
    __y: int
    __z: int

    def __init__(self, damage: str):
        # XdY[ + Z]
        m = re.search(r"^(\d+)d(\d+)( \+ (\d+))?$", damage)
        if m:
            self.__x = int(m.group(1))
            self.__y = int(m.group(2))
            z = m.group(4)
            if z:
                self.__z = int(z)
            else:
                self.__z = 0

    def draw(self):
        result = 0
        for i in range(self.__x):
            result += random.randint(1, self.__y)
        result += self.__z
        return result


class Combatant:

    name: str
    last_damage: int
    last_health: int
    health: int
    __damage: Damage

    def __init__(self, name: str, hp: int, damage: Damage):
        self.name = name
        self.health = hp
        self.__damage = damage

    def attack(self) -> int:
        self.last_damage = self.__damage.draw();
        return self.last_damage

    def get_attacked(self, damage: int) -> int:
        self.last_health = self.health
        self.health -= damage
        if self.health < 0:
            self.health = 0
        return self.health

    def is_dead(self):
        return self.health == 0


Combatants = List[Combatant]


class Arena:

    c1: Combatant
    c2: Combatant

    def __init__(self, combatants: Combatants):
        self.c1 = combatants[0]
        self.c2 = combatants[1]

    def fight(self):
        round_number: int = 1
        while not self.c1.is_dead() and not self.c1.is_dead():
            print(self.next_round(round_number, self.c1, self.c2))
            self.c1, self.c2 = self.c2, self.c1
            round_number += 1
        else:
            print('{0} won!'.format(self.c2.name))

    @staticmethod
    def next_round(round_number: int, attacker: Combatant, defender: Combatant) -> str:
        defender.get_attacked(attacker.attack())
        return '{0} {1} {2} {3} {4} {5}'\
            .format(str(round_number),
                    attacker.name,
                    defender.name,
                    str(attacker.last_damage),
                    str(defender.last_health),
                    str(defender.health))


def load_combatants() -> Combatants:
    with open('../tasks/combat/combatants.json') as f:
        combatants = json.load(f, object_hook=combatant_decoder)
    return combatants


def combatant_decoder(obj) -> Combatant:
    return Combatant(str(obj['name']), int(obj['hp']), Damage(str(obj['damage'])))


def main():
    Arena(load_combatants()).fight()


if __name__ == "__main__":
    main()