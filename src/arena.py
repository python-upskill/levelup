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
    def __init__(self):
        combatants = create_combatants()
        self.attacker = combatants[randint(0, 1)]
        combatants.remove(self.attacker)
        self.opponent = combatants[0]

    def get_winner(self):
        if self.attacker.is_won():
            return self.attacker
        if self.opponent.is_won():
            return self.opponent
        return None

    def start_battle(self):
        round_number = 1
        while True:
            self.attacker.attack(self.opponent)
            self.attacker.print_round(round_number)
            if self.get_winner():
                winner = self.get_winner()
                break
            round_number += 1
            self.attacker = self.attacker.opponent
            self.opponent = self.attacker.opponent
        print('{} wins in {} rounds!'.format(winner.name, round_number))


Arena().start_battle()

WORKS = True
