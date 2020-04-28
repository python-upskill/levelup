import jsonpickle
from combatant import Combatant
from dataclasses import dataclass


@dataclass
class Victory:
    winner: str
    round: int
    ko: bool


@dataclass
class RoundResult:
    round_number: int
    attacker: str
    defender: str
    damage: int
    previous_hp: int
    current_hp: int


class BattleResult:
    rounds: list

    def __init__(self):
        self.rounds = list()

    def add_round(self, battle_round: RoundResult):
        self.rounds.append(battle_round)

    def to_json(self):
        return jsonpickle.encode(self, unpicklable=False)


@dataclass
class Round:
    round_nr: int
    attacker: Combatant
    defender: Combatant
    damage: int

    def round_result(self) -> RoundResult:
        return RoundResult(self.round_nr,
                           self.attacker.name,
                           self.defender.name,
                           self.damage,
                           self.defender.hp + self.damage,
                           self.defender.hp)
