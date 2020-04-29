import requests
import arena
import json


def read_combatant(combatant_name: str) -> arena.Combatant:
    response: requests.Response = requests.get("https://www.dnd5eapi.co/api/monsters/" + combatant_name)
    if not response.ok:
        raise AttributeError(f"Combatant {combatant_name} not found!")
    x: json = response.json()
    return arena.Combatant(combatant_name,
                     x['hit_points'],
                     x['actions'][1]['damage'][0]['damage_dice'])
