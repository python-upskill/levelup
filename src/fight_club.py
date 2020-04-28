import json
from random import randint
from dataclasses import dataclass

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
		fighters = sorted(fighters, key=lambda fighter: fighter.hp)
		winner = fighters[-1]
		loser = fighters[0]
		ko = loser.hp <= 0;
		victory = Victory(winner.name, round_number, ko)
		return victory

	def draw_fighters_slots(self, fighters):
		first_fighter = fighters[randint(0, 1)]
		fighters.remove(first_fighter)
		second_fighter = fighters[0]
		fighters_with_drawed_slots = [first_fighter, second_fighter]
		return fighters_with_drawed_slots

	def fight(self, fighters_list: list, max_rounds_number: int) -> 'FightResult':
		round_number = 1
		rounds_summary_list = []
		fighters = self.draw_fighters_slots(fighters_list)
		while all(f.hp > 0 for f in fighters) and round_number <= max_rounds_number:
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

@dataclass
class Fighter:
	name: str
	hp: int
	damage_dice: str
	damage_bonus: int

@dataclass
class FightResult:
	rounds: list
	victory: object

@dataclass
class Victory:
	winner_name: str
	rounds_number: int
	ko: bool

@dataclass
class RoundSummary:
	round_number: int
	attacker: str
	defender: str
	damage: int
	previous_hp: int
	current_hp: int

