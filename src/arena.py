import json
import random
from combatant import Combatant


class Arena:

    def __init__(self, combatants):
        self.combatants = combatants

    def fight(self):
        game_master = random.randint(0, 1)
        round_nr = 1
        while True:
            attacker: Combatant = self.combatants[(round_nr + game_master) % 2]
            defender: Combatant = self.combatants[(round_nr + game_master + 1) % 2]

            print(f"{round_nr}", end=' ')
            attacker.attack(defender)

            if defender.is_dead():
                print(f"{attacker.name} wins in {round_nr} rounds!")
                break
            round_nr += 1


def combatant_decoder(obj):
    return Combatant(obj['name'], obj['hp'], obj['damage'])


def load_combatants():
    with open('../tasks/combat/combatants.json') as f:
        combatants = json.load(f, object_hook=combatant_decoder)
    return combatants


def main():
    combatants = load_combatants()
    arena = Arena(combatants)
    arena.fight()


if __name__ == "__main__":
    main()
