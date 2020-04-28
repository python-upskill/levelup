import random
from combatant import Combatant
from battle_result import *
from battle_request import *


class Arena:
    max_rounds: int
    combatants: list

    def __init__(self, battle_request: BattleRequest):
        self.combatants = battle_request.combatants
        self.max_rounds = battle_request.max_rounds

    def fight(self) -> BattleResult:
        game_master = random.randint(0, 1)

        battle_result = BattleResult()

        for round_nr in range(1, self.max_rounds + 1):
            attacker: Combatant = self.combatants[(round_nr + game_master) % 2]
            defender: Combatant = self.combatants[(round_nr + game_master + 1) % 2]

            previous_hp = defender.hp

            print(f"{round_nr}", end=' ')
            attacker.attack(defender)

            round_result = RoundResult(round_nr, attacker.name,
                                       defender.name, previous_hp - defender.hp,
                                       previous_hp, defender.hp)

            battle_result.add_round(round_result)

            if defender.is_dead():
                print(f"{attacker.name} wins in {round_nr} rounds!")
                break

        winner: Combatant
        if defender.hp > attacker.hp:
            winner = defender
        else:
            winner = attacker

        victory = Victory(winner.name, round_nr, self.__is_ko())
        battle_result.victory = victory

        return battle_result

    def __is_ko(self):
        for c in self.combatants:
            if c.hp <= 0:
                return True
        return False
