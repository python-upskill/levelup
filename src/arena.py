from util import json_operations
from combatants import *
from random import randint
from io import StringIO


class Arena:
    attacker: Combatant
    opponent: Combatant
    battle_reporter: 'BattleReporter'
    combatants_retriever = CombatantsRetriever()
    max_rounds: int

    def __init__(self, battle_reporter: 'BattleReporter', max_rounds: int = None):
        self.battle_reporter = battle_reporter
        self.max_rounds = max_rounds

    def retrieve_combatants(self):
        return self.combatants_retriever.from_file('../tasks/combat/combatants.json')

    def init(self):
        combatants = self.retrieve_combatants()
        self.attacker = combatants[randint(0, 1)]
        combatants.remove(self.attacker)
        self.opponent = combatants[0]

    def get_winner(self) -> Combatant:
        if self.attacker.is_lost():
            return self.opponent
        if self.opponent.is_lost():
            return self.attacker
        return None

    def get_current_winner(self) -> Combatant:
        if self.attacker.hp_after_attack >= self.opponent.hp_after_attack:
            return self.attacker
        return self.opponent

    def get_summary(self):
        return self.battle_reporter.get_summary()

    def is_finished_by_round_nr(self, round_nr: int) -> bool:
        return self.max_rounds and round_nr > self.max_rounds

    def start_battle(self):
        round_nr = 1
        winner = None
        while not self.is_finished_by_round_nr(round_nr) and not winner:
            self.attacker.attack(self.opponent)
            self.battle_reporter.take_snapshot(self)
            winner = self.get_winner()
            round_nr += 1
            self.attacker, self.opponent = self.opponent, self.attacker
        if winner:
            self.battle_reporter.finish_battle_by_ko(winner.name)
        else:
            self.battle_reporter.finish_battle(winner.name)
        print(json_operations.toJSON(self.battle_reporter))


class Victory:
    winner: str
    rounds: int
    ko: bool

    def __init__(self):
        self.ko = False


class BattleReporter:
    rounds: list
    victory: Victory

    def __init__(self):
        self.rounds = []
        self.victory = Victory()

    def get_incoming_round_number(self):
        return self.rounds.__len__() + 1

    def get_finished_rounds_count(self):
        return self.rounds.__len__()

    def take_snapshot(self, arena: Arena) -> None:
        incoming_round_nr = self.get_finished_rounds_count() + 1
        self.rounds.append(RoundResult(incoming_round_nr, arena.attacker,
                                       arena.opponent))

    def _get_winner(self) -> Combatant:
        return self.rounds[-1].attacker

    def get_summary(self) -> str:
        writer = StringIO()
        for r in self.rounds:
            writer.write(f'{r.get_description()}\n')
        rounds_count = self.get_finished_rounds_count()
        writer.write(f'{self._get_winner()} wins in {rounds_count} rounds!')
        result = writer.getvalue()
        writer.close()
        return result

    def finish_battle(self, winner_name: str):
        self.victory.winner = winner_name
        self.victory.rounds = self.get_finished_rounds_count()

    def finish_battle_by_ko(self, winner_name: str):
        self.finish_battle(winner_name)
        self.victory.ko = True


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


if __name__ == "__main__":
    arena = Arena(BattleReporter())
    arena.init()
    arena.start_battle()
    print(arena.get_summary())
