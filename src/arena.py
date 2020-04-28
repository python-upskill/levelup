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


class Round:
    round_number: str
    attacker: str
    defender: str
    damage: int
    previous_hp: int
    current_hp: int

    def __init__(self, round_number: str,
                 attacker: str, defender: str, damage: int,
                 previous_hp: int, current_hp: int):
        self.round_number = round_number
        self.attacker = attacker
        self.defender = defender
        self.damage = damage
        self.previous_hp = previous_hp
        self.current_hp = current_hp


Rounds = List[Round]


class Victory:
    winner: str
    rounds: int
    ko: bool

    def __init__(self, winner: str,
                 rounds: int,
                 ko: bool):
        self.winner = winner
        self.rounds = rounds
        self.ko = ko


class Result:
    rounds: Rounds
    victory: Victory

    def __init__(self, rounds: Rounds, victory: Victory):
        self.rounds = rounds
        self.victory = victory


class Arena:
    c1: Combatant
    c2: Combatant
    max_rounds: int

    def __init__(self, c1: Combatant, c2: Combatant, max_rounds: int):
        self.c1 = c1
        self.c2 = c2
        self.max_rounds = max_rounds

    def fight(self) -> Result:
        rounds: Rounds = []
        victory: Victory
        round_number: int = 1
        while not self.c1.is_dead() and not self.c1.is_dead() and round_number <= self.max_rounds:
            rounds.append(self.next_round(round_number, self.c1, self.c2))
            self.c1, self.c2 = self.c2, self.c1
            round_number += 1
        else:
            print('{0} won!'.format(self.c2.name))
            victory = Victory(self.c2.name, round_number - 1, self.c1.is_dead())
        return Result(rounds, victory)

    @staticmethod
    def next_round(round_number: int, attacker: Combatant, defender: Combatant) -> Round:
        defender.get_attacked(attacker.attack())
        print('{0} {1} {2} {3} {4} {5}' \
              .format(str(round_number),
                      attacker.name,
                      defender.name,
                      str(attacker.last_damage),
                      str(defender.last_health),
                      str(defender.health)))
        return Round(round_number,
                     attacker.name,
                     defender.name,
                     attacker.last_damage,
                     defender.last_health,
                     defender.health)


def load_combatants() -> Combatants:
    with open('../tasks/combat/combatants.json') as f:
        combatants = json.load(f, object_hook=combatant_decoder)
    return combatants


def combatant_decoder(obj) -> Combatant:
    return Combatant(str(obj['name']), int(obj['hp']), Damage(str(obj['damage'])))


def main():
    combatants: Combatants = load_combatants()
    Arena(combatants[0], combatants[1], 10).fight()


if __name__ == "__main__":
    main()
