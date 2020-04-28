from combatant import Combatant
import requests


class CombatantRepository:

    @classmethod
    def get(cls, name: str) -> Combatant:
        data = requests.get(f"https://www.dnd5eapi.co/api/monsters/{name}")
        if data.status_code != 200:
            raise ValueError(f"Combatant with name [{name}] does not exist.")
        json_data = data.json()

        return cls.__combatant_decoder(json_data)

    @classmethod
    def __combatant_decoder(cls, json_data) -> Combatant:
        return Combatant(json_data['name'], json_data['hit_points'], cls.__get_damage(json_data))

    @classmethod
    def __get_damage(cls, json_data) -> str:
        for action in json_data['actions']:
            if 'damage' in action:
                return action['damage'][0]['damage_dice']
        return None
