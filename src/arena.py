import json
import random
import re
import requests
from json import JSONEncoder
from typing import List
from wsgiref import simple_server
import marshmallow_dataclass

import falcon
from dataclasses import dataclass, field


class Combatant:

    def __init__(self, name: str, hp: int, damage: str):
        self.name = name
        self.health = hp
        self.__damage = self.Damage(damage)
        self.last_damage = 0
        self.last_health = hp

    def attack(self, other: 'Combatant'):
        self.last_damage = self.__damage.draw()
        other.__get_attacked(self.last_damage)

    def __get_attacked(self, damage: int):
        self.last_health = self.health
        self.health -= damage
        if self.health < 0:
            self.health = 0

    def is_dead(self) -> bool:
        return self.health == 0

    class Damage:
        __dice_roll_number: int
        __dice_sides_number: int
        __attack_bonus: int

        def __init__(self, damage: str):
            # XdY[ + Z]
            m = re.search(r"^(\d+)d(\d+)( \+ (\d+))?$", damage)
            if m:
                self.__dice_roll_number = int(m.group(1))
                self.__dice_sides_number = int(m.group(2))
                z = m.group(4)
                if z:
                    self.__attack_bonus = int(z)
                else:
                    self.__attack_bonus = 0

        def draw(self):
            result = 0
            for i in range(self.__dice_roll_number):
                result += random.randint(1, self.__dice_sides_number)
            result += self.__attack_bonus
            return result


Combatants = List[Combatant]


class Arena:
    c1: Combatant
    c2: Combatant
    max_rounds: int

    def __init__(self, c1: Combatant, c2: Combatant, max_rounds: int):
        self.c1 = c1
        self.c2 = c2
        self.max_rounds = max_rounds

    def fight(self) -> 'BattleResult':
        rounds: 'BattleResult.Rounds' = []
        victory: 'BattleResult.Victory'
        round_number: int = 1
        while not self.c1.is_dead() and not self.c1.is_dead() and round_number <= self.max_rounds:
            rounds.append(self.next_round(round_number, self.c1, self.c2))
            self.c1, self.c2 = self.c2, self.c1
            round_number += 1
        else:
            if self.c1.health > self.c2.health:
                victory = self.BattleResult.Victory(self.c1.name, round_number - 1, self.c2.is_dead())
            else:
                victory = self.BattleResult.Victory(self.c2.name, round_number - 1, self.c1.is_dead())
        print(f'{victory.winner} won!')
        return self.BattleResult(rounds, victory)

    def next_round(self, round_number: int, attacker: Combatant, defender: Combatant) -> 'Round':
        attacker.attack(defender)
        print(f'{str(round_number)} {attacker.name} {defender.name} {str(attacker.last_damage)} '
              f'{str(defender.last_health)} {str(defender.health)}')
        return self.BattleResult.Round(round_number,
                                       attacker.name,
                                       defender.name,
                                       attacker.last_damage,
                                       defender.last_health,
                                       defender.health)

    @dataclass
    class BattleResult:

        rounds: 'Rounds'
        victory: 'Victory'

        @dataclass
        class Round:
            round_number: str
            attacker: str
            defender: str
            damage: int
            previous_hp: int
            current_hp: int

        Rounds = List['Battle.Round']

        @dataclass
        class Victory:
            winner: str
            rounds: int
            ko: bool


class CombatantsLoader:

    def load_combatants(self, combatant_1_name: str, combatant_2_name: str) -> Combatants:
        return [self.__load_combatant(combatant_1_name), self.__load_combatant(combatant_2_name)]

    def __load_combatant(self, combatant_name: str) -> Combatants:
        response: requests.Response = requests.get("https://www.dnd5eapi.co/api/monsters/" + combatant_name)
        if not response.ok:
            raise AttributeError(f"Combatant {combatant_name} not found!")
        monster: 'Monster' = marshmallow_dataclass.class_schema(self.Monster).load(json.load(response.content))
        damage: 'Monster.Action.Damage' = next(i for i in len(monster.actions)
                                        if monster.actions[i].damage.damage_dice is not None)
        return Combatant(combatant_name, monster.hit_points, damage.damage_dice)

    @dataclass
    class Monster:
        hit_points: int
        actions: List['Monster.Action']

        @dataclass
        class Action:
            damage: 'Damage'

            @dataclass
            class Damage:
                damage_dice: str
                damage_bonus: str


class ArenaResource:

    def on_post(self, req, resp):
        resp.status = falcon.HTTP_200
        combatants: Combatants = CombatantsLoader().load_combatants("orc", "orc")
        resp.body = json.dumps(Arena(combatants[0], combatants[1], 10).fight(), cls=self.BattleResultEncoder)

    class BattleResultEncoder(JSONEncoder):
        def default(self, o):
            return o.__dict__


app = falcon.API()
app.add_route('/fight', ArenaResource())

if __name__ == "__main__":
    httpd = simple_server.make_server('127.0.0.1', 7011, app)
    httpd.serve_forever()
