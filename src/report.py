from util import json_operations
from combatants.retriever import *
from dataclasses import dataclass
from db.query import *
from typing import *


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

    def _cache_round_result(self, round_result: 'RoundResult'):
        self.rounds.append(round_result)

    def take_snapshot(self, attacker: Combatant, opponent: Combatant) -> None:
        incoming_round_nr = self.get_finished_rounds_count() + 1
        self._cache_round_result(RoundResult(incoming_round_nr, attacker, opponent))

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


class DbCache:
    combatant_entities = {}
    battle_entity: BattleEntity
    combatant_query = CombatantQuery()
    battle_query = BattleQuery()

    def _cache_combatant_by_name(self, name: str) -> None:
        entity = self.combatant_query.find_first_by_name(name)
        self.combatant_entities.setdefault(name, entity)

    def from_round_result(self, round_result: 'RoundResult') -> 'DbCache':
        self._cache_combatant_by_name(round_result.attacker)
        self._cache_combatant_by_name(round_result.defender)
        return self

    def from_battle_id(self, id: int) -> 'DbCache':
        self.battle_entity = self.battle_query.find_by_id(id)
        return self


class DbJsonBattleReporter(JsonBattleReporter):
    db_cache = DbCache()
    # round_entities = List[RoundEntity]
    # combatant_state_entities = List[CombatantStateEntity]
    # CombatantEntity
    # combatant_entities = {}

    # def create_battle_in_db(self):
    #

    def save_battle(self):
        self.db_cache.from_battle_id(BattleEntity().create().save())

    def _cache_round_result(self, round_result: 'RoundResult'):
        self.db_cache.from_round_result(round_result)
        attacker_id = self.db_cache.combatant_entities[round_result.attacker]
        opponent_id = self.db_cache.combatant_entities[round_result.defender]
        round_entity = RoundEntity

    def get_summary(self) -> str:
        return super().get_summary()

    # def _save_round_result(self, round_result: 'RoundResult'):
        # CombatantQuery().
        # mapper = ToEntityMapper()
        # mapper.m


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


# d = {}
# d.setdefault('a','v1')
# d.setdefault('a','v2')
# print(d)
# print(d.setdefault('a','v1'))
# print(d.setdefault('a','v2'))