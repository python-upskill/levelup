import requests
import arena
import json


def read_combatant(combatant_name: str) -> arena.Combatant:
    response: requests.Response = requests.get("https://www.dnd5eapi.co/api/monsters/" + combatant_name)
    if response.status_code != 200:
        raise AttributeError(f"Combatant {combatant_name} not found!")
    response_json: json = response.json()
    return arena.Combatant(combatant_name,
                           response_json['hit_points'],
                           __get_damage_dice(response_json['actions']))


def __get_damage_dice(actions) -> str:
    for action in actions:
        if 'damage' in action:
            for damage_item in action['damage']:
                if 'damage_dice' in damage_item:
                    return damage_item['damage_dice'] \
                           + ((" + " + str(damage_item['damage_bonus']))
                              if ('damage_bonus' in damage_item) else "")
