import random
import re


class Combatant:
    def __init__(self, name: str, hp: int, damage: str):
        self.name = name
        self.hp = hp
        self.damage = Damage(damage)

    def attack(self, defender: 'Combatant'):
        damage = self.damage.draw_damage()
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
        m = re.search(r"(\d+)d(\d+)(\[ \+ (\d+)\])*", damage)
        if m:
            self.x = int(m.group(1))
            self.y = int(m.group(2))
            z = m.group(4)
            if z:
                self.z = int(z)

    def draw_damage(self):
        result = 0
        for __i in range(self.x):
            result += random.randint(1, self.y)

        result += self.z

        return result
