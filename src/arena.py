from combatants import *
from random import randint
from io import StringIO


class Arena:
    attacker: Combatant
    opponent: Combatant
    battle_reporter: 'BattleReporter'
    combatants_retriever = CombatantsRetriever()

    def __init__(self, battle_reporter: 'BattleReporter'):
        self.battle_reporter = battle_reporter

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

    def print_round(self, round_number: int) -> None:
        print(f'{round_number} {self.attacker.name} {self.opponent.name} {self.attacker.damage} '
              f'{self.opponent.hp_before_attack} {self.opponent.hp_after_attack}')

    def start_battle(self):
        winner = None
        while not winner:
            self.attacker.attack(self.opponent)
            self.battle_reporter.take_snapshot(self)
            winner = self.get_winner()
            self.attacker, self.opponent = self.opponent, self.attacker
        print(self.battle_reporter.get_summary())


class BattleReporter:
    round_results = []

    def get_incoming_round_number(self):
        return self.round_results.__len__() + 1

    def take_snapshot(self, arena: Arena) -> None:
        round_number = self.get_incoming_round_number()
        self.round_results.append(RoundResult(round_number, arena.attacker,
                                              arena.opponent))

    def _get_winner(self) -> Combatant:
        return self.round_results[-1].attacker

    def get_summary(self) -> str:
        writer = StringIO()
        for r in self.round_results:
            writer.write(f'{r.get_description()}\n')
        rounds_count = self.get_incoming_round_number() - 1
        writer.write(f'{self._get_winner().name} wins in {rounds_count} rounds!')
        result = writer.getvalue()
        writer.close()
        return result


class RoundResult:
    round_number: int
    attacker: Combatant
    opponent: Combatant

    def __init__(self, round_number: int, attacker: Combatant, opponent: Combatant):
        self.round_number = round_number
        self.attacker = attacker
        self.opponent = opponent

    def get_description(self) -> str:
        return (f'{self.round_number} {self.attacker.name} {self.opponent.name} '
                f'{self.attacker.damage} {self.opponent.hp_before_attack} '
                f'{self.opponent.hp_after_attack}')


if __name__ == "__main__":
    arena = Arena(BattleReporter())
    arena.init()
    arena.start_battle()
