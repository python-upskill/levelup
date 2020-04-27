import re
from util.json_operations import *
from random import randint


class DiceSimulator:
    rolls_number = 0
    dice_sides = 0
    extra_param = 0

    def encode(self, expr: str) -> 'DiceSimulator':
        matcher = re.search(r'(\d+)d(\d+)(\s+\+\s+(\d+))*', expr)
        if matcher:
            self.rolls_number = int(matcher.group(1))
            self.dice_sides = int(matcher.group(2))
            extra_param = matcher.group(4)
            if extra_param:
                self.extra_param = int(extra_param)
        return self

    def random_result(self) -> int:
        result = 0
        for _ in range(self.rolls_number):
            result += randint(1, self.dice_sides)
        return result + self.extra_param


class Combatant(object):
    name: str
    hp_before_attack: int
    hp_after_attack: int
    damage: int
    dice_simulator: DiceSimulator

    def __init__(self, name: str, hp: int, damage: str):
        self.name = name
        self.hp_before_attack = hp
        self.hp_after_attack = hp
        self.dice_simulator = DiceSimulator().encode(damage)

    def _random_damage(self) -> int:
        return self.dice_simulator.random_result()

    def attack(self, other: 'Combatant') -> None:
        other.hp_before_attack = other.hp_after_attack
        self.damage = self._random_damage()
        other.hp_after_attack -= self.damage

    def is_lost(self) -> bool:
        return self.hp_after_attack <= 0


class CombatantsRetriever:

    json_retriever = JsonRetriever()

    def _create_combatants(self, json_elements: list):
        result = []
        for e in json_elements:
            result.append(Combatant(**e))
        return result

    def from_file(self, path: str):
        return self._create_combatants(self.json_retriever.from_file(path))

    def from_url(self, url: str):
        return self._create_combatants(self.json_retriever.from_url(url))