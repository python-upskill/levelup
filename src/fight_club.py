import json
from random import randint

WORKS = True

class FightClub:
	def __calculate_damage_dice(self, damage_dice_pattern):
		damage_factors = damage_dice_pattern.split('d')
		multiplier = int(damage_factors[0])
		damage_range = int(damage_factors[1])
		damage = 0;
		for __index in range(multiplier):
			damage += randint(1, damage_range)
		return damage

	def __calculate_damage(self, fighter):
		damage_dice = self.__calculate_damage_dice(fighter.damage_dice)
		damage = damage_dice + fighter.damage_bonus
		return damage

	def __sum_up_fight(self, fighters, round_number):
		winner = fighters[0] if fighters[0].hp > fighters[1].hp else fighters[1]
		fighters.remove(winner)
		defender = fighters[0]
		ko = defender.hp <= 0;
		victory = Victory(winner.name, round_number, ko)
		return victory


	def fight(self, fighters, max_rounds_number):
		round_number = 1
		rounds_summary_list = []
		while fighters[0].hp > 0 and fighters[1].hp > 0 and round_number <= max_rounds_number:
			attacker = fighters[round_number % 2]
			defender = fighters[(round_number + 1) % 2]
			damage = self.__calculate_damage(attacker)
			defender_previous_hp = defender.hp
			defender.hp = defender_previous_hp - damage
			print(f"{round_number} {attacker.name} {defender.name} "
				f"{damage} {defender_previous_hp} {defender.hp}")
			round_summary = RoundSummary(round_number, attacker.name, defender.name, damage, defender_previous_hp, defender.hp)
			rounds_summary_list.append(round_summary)
			round_number += 1
		victory = self.__sum_up_fight(fighters, round_number)
		fight_result = FightResult(rounds_summary_list, victory)
		return fight_result

class Fighter:
	def __init__(self, name: str, hp: int, damage_dice: str, damage_bonus: int):
		self.name = name
		self.hp = hp
		self.damage_dice = damage_dice
		self.damage_bonus = damage_bonus

class FightResult:
	def __init__(self, rounds: list, victory: object):
		self.rounds = rounds
		self.victory = victory

class Victory:
	def __init__(self, winner_name: str, rounds_number: int, ko: bool):
		self.winner_name = winner_name
		self.rounds_number = rounds_number
		self.ko = ko

class RoundSummary:
	def __init__(self, round_number: int, attacker: str, defender: str, damage: int, previous_hp: int, current_hp: int):
		self.round_number = round_number
		self.attacker = attacker
		self.defender = defender
		self.damage = damage
		self.previous_hp = previous_hp
		self.current_hp = current_hp

