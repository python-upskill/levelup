import random
import re
from typing import List
from dataclasses import dataclass


class Combatant:

    def __init__(self, name: str, health: int, damage: str):
        self.name = name
        self.health = health
        self.__damage = self.Damage(damage)
        self.last_damage = 0
        self.last_health = health

    @property
    def damage(self) -> str:
        return self.__damage.to_string()

    def attack(self, other: 'Combatant'):
        self.last_damage = self.__damage.draw()
        other.__get_attacked(self.last_damage)

    def __get_attacked(self, damage: int):
        self.last_health = self.health
        self.health -= damage
        if self.health < 0:
            self.health = 0

    @property
    def is_dead(self) -> bool:
        return self.health == 0

    class Damage:
        __dice_roll_number: int
        __dice_sides_number: int
        __attack_bonus: int

        def __init__(self, damage: str):
            # XdY[ + Z]
            m = re.search(r"^(\d+)d(\d+)( \+ (\d+))?$", damage)
            if m:
                self.__dice_roll_number = int(m.group(1))
                self.__dice_sides_number = int(m.group(2))
                z = m.group(4)
                if z:
                    self.__attack_bonus = int(z)
                else:
                    self.__attack_bonus = 0

        def to_string(self) -> str:
            return str(self.__dice_roll_number) \
                   + "d" \
                   + str(self.__dice_sides_number) \
                   + ((" + " + str(self.__attack_bonus)) if self.__attack_bonus != 0 else "")

        def draw(self):
            result = 0
            for i in range(self.__dice_roll_number):
                result += random.randint(1, self.__dice_sides_number)
            result += self.__attack_bonus
            return result


Combatants = List[Combatant]


@dataclass
class BattleResult:
    rounds: 'Rounds'
    victory: 'Victory'

    @dataclass
    class Round:
        round_number: int
        attacker: str
        defender: str
        damage: int
        previous_hp: int
        current_hp: int

    Rounds = List['BattleResult.Round']

    @dataclass
    class Victory:
        winner: str
        rounds: int
        ko: bool


BattleResults = List[BattleResult]


class Arena:
    c1: Combatant
    c2: Combatant
    max_rounds: int

    def __init__(self, c1: Combatant, c2: Combatant, max_rounds: int):
        self.c1 = c1
        self.c2 = c2
        self.max_rounds = max_rounds

    def fight(self) -> 'BattleResult':
        rounds: BattleResult.Rounds = []
        victory: BattleResult.Victory
        round_number: int = 1
        while not self.c1.is_dead and not self.c1.is_dead and round_number <= self.max_rounds:
            rounds.append(self.__next_round(round_number, self.c1, self.c2))
            self.c1, self.c2 = self.c2, self.c1
            round_number += 1
        else:
            if self.c1.health > self.c2.health:
                victory = BattleResult.Victory(self.c1.name, round_number - 1, self.c2.is_dead)
            else:
                victory = BattleResult.Victory(self.c2.name, round_number - 1, self.c1.is_dead)
        print(f'{victory.winner} won!')
        return BattleResult(rounds, victory)

    @staticmethod
    def __next_round(round_number: int, attacker: Combatant, defender: Combatant) -> 'Round':
        attacker.attack(defender)
        print(f'{str(round_number)} {attacker.name} {defender.name} {str(attacker.last_damage)} '
              f'{str(defender.last_health)} {str(defender.health)}')
        return BattleResult.Round(round_number,
                                  attacker.name,
                                  defender.name,
                                  attacker.last_damage,
                                  defender.last_health,
                                  defender.health)
