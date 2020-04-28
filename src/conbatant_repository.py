from combatant import Combatant
import requests


class CombatantRepository:

    @staticmethod
    def get(name: str) -> Combatant:
        data = requests.get(f"https://www.dnd5eapi.co/api/monsters/{name}")
        if data.status_code != 200:
            raise ValueError(f"Combatant with name [{name}] does not exist.")
        json_data = data.json()

        return CombatantRepository.__combatant_decoder(json_data)

    @staticmethod
    def __combatant_decoder(json_data) -> Combatant:
        return Combatant(json_data['name'], json_data['hit_points'], CombatantRepository.__get_damage(json_data))

    @staticmethod
    def __get_damage(json_data) -> str:
        for action in json_data['actions']:
            if 'damage' in action:
                for damage in action['damage']:
                    return damage['damage_dice']
        return None
