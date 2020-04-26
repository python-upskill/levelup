import json
import random
import re


class Combatant:
    def __init__(self, name: str, hp: int, damage: str):
        self.name = name
        self.hp = hp
        self.damage = Damage(damage)

    def attack(self, defender: 'Combatant'):
        damage = self.damage.draw_demage()
        defender.deal_a_blow(damage)
        print(f"{self.name} {defender.name} {damage} {defender.hp + damage} {defender.hp}")

    def deal_a_blow(self, demage: int):
        self.hp -= demage

    def is_dead(self):
        return self.hp <= 0


class Damage:
    x = 0
    y = 0
    z = 0

    def __init__(self, damage):
        # XdY[ + Z]
        m = re.search('(\d+)d(\d+)(\[ \+ (\d+)\])*', damage)
        if m:
            self.x = int(m.group(1))
            self.y = int(m.group(2))
            z = m.group(4)
            if z:
                self.z = int(z)

    def draw_demage(self):
        dice = random.randint(1, self.x)
        result = 0
        for i in range(dice):
            result += random.randint(1, self.y)

        result += self.z

        return result


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
                quit()
            round_nr += 1


def combatant_decoder(obj):
    return Combatant(obj['name'], obj['hp'], obj['damage'])
    return obj


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
