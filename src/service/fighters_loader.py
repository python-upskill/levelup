import requests

from dto.fighter_dto import FighterDto
from repository.fighter_repository import FighterRepository


class FightersLoader:
    @classmethod
    def load_fighter(name: str):
        data = requests.get(f"https://www.dnd5eapi.co/api/monsters/{name}")
        json_data = data.json()
        if "error" in json_data:
            raise AttributeError(f"Fighter {name} not found in database!")
        return FightersLoader.extract_fighter_details(json_data)

    @classmethod
    def extract_fighter_details(cls, json_data):
        name = json_data["name"]
        hp = json_data["hit_points"]
        for action in json_data["actions"]:
            if "damage" in action:
                for damage in action["damage"]:
                    if "damage_dice" in damage:
                        damage_dice = damage["damage_dice"]
                        damage_bonus = FightersLoader.extract_fighter_damage_bonus(
                            damage
                        )
                        return FighterDto(name, hp, damage_dice, damage_bonus)
        raise AttributeError(f"Fighter {name} doesn't have any damage points defined!")

    @classmethod
    def extract_fighter_damage_bonus(cls, damage):
        if "damage_bonus" in damage:
            return damage["damage_bonus"]
        return 0

    @staticmethod
    def load_fighters(fighters_indexes):
        fighters = []
        for index in fighters_indexes:
            fighter = FighterRepository.find_fighter_by_index(index)
            if fighter is None:
                fighter = FightersLoader.load_fighter(index)
                FighterRepository.save_fighter(index, fighter)
            fighters.append(fighter)
        return fighters
