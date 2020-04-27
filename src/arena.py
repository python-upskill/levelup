from combatants import Combatant
from util import json_operations
from random import randint


def create_combatants(path='../tasks/combat/combatants.json'):
    elements = json_operations.read_from_file(path)
    result = []
    for e in elements:
        result.append(Combatant(**e))
    return result


class Arena:
    attacker: Combatant
    opponent: Combatant

    def __init__(self):
        combatants = create_combatants()
        self.attacker = combatants[randint(0, 1)]
        combatants.remove(self.attacker)
        self.opponent = combatants[0]
        self.attacker.opponent = self.opponent
        self.opponent.opponent = self.attacker

    def get_winner(self) -> Combatant:
        if self.attacker.is_winner():
            return self.attacker
        if self.opponent.is_winner():
            return self.opponent
        return None

    def swap_combatants(self) -> None:
        self.attacker = self.attacker.opponent
        self.opponent = self.attacker.opponent

    def start_battle(self):
        round_number = 0
        winner = None
        while not winner:
            round_number += 1
            self.attacker.attack(self.opponent)
            self.attacker.print_round(round_number)
            winner = self.get_winner()
            self.swap_combatants()
        print(f'{winner.name} wins in {round_number} rounds!')


if __name__ == "__main__":
    Arena().start_battle()
