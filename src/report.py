from util import json_operations
from combatants import *
from dataclasses import dataclass


@dataclass
class Victory:
    winner: str = None
    rounds: int = None
    ko: bool = False


class BattleReporter:
    rounds: list
    victory: Victory

    def __init__(self):
        self.rounds = []
        self.victory = Victory()

    def get_finished_rounds_count(self):
        return self.rounds.__len__()

    def take_snapshot(self, attacker: Combatant, opponent: Combatant) -> None:
        incoming_round_nr = self.get_finished_rounds_count() + 1
        self.rounds.append(RoundResult(incoming_round_nr, attacker, opponent))

    def _get_winner(self) -> Combatant:
        return self.rounds[-1].attacker

    def get_summary(self) -> str:
        return "\n".join(list(map(lambda r: r.get_description(), self.rounds)))

    def finish_battle(self, winner_name: str):
        self.victory.winner = winner_name
        self.victory.rounds = self.get_finished_rounds_count()

    def finish_battle_by_ko(self, winner_name: str):
        self.finish_battle(winner_name)
        self.victory.ko = True


class JsonBattleReporter(BattleReporter):
    def get_summary(self) -> str:
        return json_operations.toJSON(self)


class RoundResult:
    round: int
    attacker: str
    defender: str
    damage: int
    previous_hp: int
    current_hp: int

    def __init__(self, round_number: int, attacker: Combatant, opponent: Combatant):
        self.round = round_number
        self.attacker = attacker.name
        self.defender = opponent.name
        self.damage = attacker.damage
        self.previous_hp = opponent.hp_before_attack
        self.current_hp = opponent.hp_after_attack

    def get_description(self) -> str:
        return (f'{self.round} {self.attacker} {self.defender} '
                f'{self.damage} {self.previous_hp} '
                f'{self.current_hp}')