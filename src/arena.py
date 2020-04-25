WORKS = True

from combatants import Combatant
from util import json_operations
from random import randint

class Arena:
    def __create_combatants(self, path='../tasks/combat/combatants.json'):
        elements = json_operations.read_from_file(path)
        result = []
        for e in elements:
            result.append(Combatant(**e))
        return result

    def __init_round(self):
        combatants = self.__create_combatants()
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
        # combatants = self.create_combatants()
        # attacker_index = randint(0,1)
        # attacker = combatants[attacker_index]
        # combatants.remove(attacker)
        # opponent = combatants[0]

        # current_attacker.opponent = opponent
        # opponent.opponent = attacker
        # print(str(type(attacker)))
        # print(str(type(opponent)))

        # attacker.
        self.__init_round()
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

# c = Arena().start_battle()
Arena().start_battle()

# print(str(type(c[0])))

# t = ['a','b']
# print(len(t[0]))
#
# combatants = Arena().create_combatants()
# attacker_index = randint(0,1)
# # attacker = combatants[int(attacker_index)]
# attacker = combatants[attacker_index]
# print(attacker.name)
# combatants.remove(attacker)
# print(combatants[0].name)
# # attacker.is_won()
# # attacker = combatants[0]
# # print(type(randint(0,1)))
#
# # Arena().start_battle()
# print('### {}',hasattr(Arena(), 'start_battle'))
# a= Arena()
# # a.x=1
# # print((hasattr(a, 'x') & a.x > 0))