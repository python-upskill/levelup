import json
import random

WORKS = True


def calculate_main_damage(damage_pattern):
    damage_factors = damage_pattern.split("d")
    multiplier = int(damage_factors[0])
    damage_range = int(damage_factors[1])
    damage = 0
    for __index in range(multiplier):
        damage += random.randint(1, damage_range)
    return damage


def calculate_damage(damage_pattern):
    damage_factors = damage_pattern.replace(" ", "").split("+")
    damage = int(damage_factors[1]) if len(damage_factors) > 1 else 0
    main_damage = calculate_main_damage(damage_factors[0])
    damage += main_damage
    return damage


with open("monsters.json", "r") as file:
    monsters = json.load(file)

round_number = 1
while int(monsters[0]["hp"]) > 0 and int(monsters[1]["hp"]) > 0:
    attacker = monsters[round_number % 2]
    defender = monsters[(round_number + 1) % 2]
    damage = calculate_damage(attacker["damage"])
    defender_previous_hp = int(defender["hp"])
    defender["hp"] = defender_previous_hp - damage
    print(
        f"{round_number} {attacker['name']} {defender['name']} "
        f"{damage} {defender_previous_hp} {defender['hp']}"
    )
    round_number += 1