from combatant import Combatant
from db.entities import CombatantEntity
import peewee
import requests


class CombatantRepository:

    @classmethod
    def get(cls, name: str) -> Combatant:

        entity: CombatantEntity = CombatantEntity.get_or_none(peewee.fn.Lower(CombatantEntity.name) == name.lower())
        if entity:
            return Combatant(entity.name, entity.hp, entity.damage_pattern)
        else:
            combatant: Combatant = cls.__load_combat_via_rest(name)
            entity: CombatantEntity = CombatantEntity()
            entity.name = combatant.name
            entity.hp = combatant.hp
            entity.damage_pattern = combatant.damage
            entity.save(force_insert=True)

            return combatant

    @classmethod
    def __load_combat_via_rest(cls, name: str) -> Combatant:
        data = requests.get(f"https://www.dnd5eapi.co/api/monsters/{name}")
        if data.status_code != 200:
            raise ValueError(f"Combatant with name [{name}] does not exist.")

        json_data = data.json()
        combatant: Combatant = cls.__combatant_decoder(json_data)
        return combatant

    @classmethod
    def __combatant_decoder(cls, json_data) -> Combatant:
        return Combatant(json_data['name'], json_data['hit_points'], cls.__get_damage(json_data))

    @classmethod
    def __get_damage(cls, json_data) -> str:
        for action in json_data['actions']:
            if 'damage' in action:
                return action['damage'][0]['damage_dice']
        return None
