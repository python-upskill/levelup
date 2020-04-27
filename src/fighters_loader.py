import requests
from fight_club import Fighter

WORKS = True

class FightersLoader:
	@staticmethod
	def load_fighter(name):
		data = requests.get(f"https://www.dnd5eapi.co/api/monsters/{name}")
		json_data = data.json()
		if("error" in json_data):
			raise AttributeError(f"Fighter {name} not found in database!")
		fighter = FightersLoader.extract_fighter_details(json_data)
		return fighter

	@staticmethod
	def extract_fighter_details(json_data):
		name = json_data["name"]
		hp = json_data["hit_points"]
		index = 0
		for action in json_data["actions"]:
			if("damage" in action):
				for damage in action["damage"]:
					if("damage_dice" in damage):
						damage_dice = damage["damage_dice"]
						damage_bonus = FightersLoader.extract_fighter_damage_bonus(damage)
						fighter = Fighter(name, hp, damage_dice, damage_bonus)
						return fighter
		raise AttributeError(f"Fighter {name} doesn't have any damage points defined!")

	@staticmethod
	def extract_fighter_damage_bonus(damage):
		if("damage_bonus" in damage):
			return  damage["damage_bonus"]
		return 0