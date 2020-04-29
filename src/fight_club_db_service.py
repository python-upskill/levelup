from model import *
import operator
from functools import reduce

class FightClubDbService:
	fighter_parameters_map = {
		'index': Fighter.index,
		'name': Fighter.name,
		'hp': Fighter.hp,
		'damage_dice': Fighter.damage_dice,
		'damage_bonus': Fighter.damage_bonus
	}

	fight_parameters_map = {
		'winner': Fight.winner,
		'rounds_number': Fight.rounds_number,
		'ko': Fight.ko
	}

	round_parameters_map = {
		'fight_id': Round.fight_id,
		'round_nr': Round.round_nr,
		'attacker': Round.attacker,
		'defender': Round.defender,
		'damage': Round.damage,
		'previous_hp': Round.previous_hp,
		'current_hp': Round.current_hp
	}

	@staticmethod
	def find_fighter_by_index(index: str) -> 'Fighter':
		fighter = Fighter.get_or_none(Fighter.index == index)
		return fighter

	@staticmethod
	def save_fighter(fighter_index: str, dto: 'FighterDto'):
		Fighter.create(index=fighter_index, **dataclasses.asdict(dto))
    
	@staticmethod
	def save_fight_result(fight_result: 'FightResultDto'):
		fight = Fight.create(winner=fight_result.victory.winner_name, rounds_number=fight_result.victory.rounds_number, ko=fight_result.victory.ko)
		for round in fight_result.rounds:
			Round.create(fight_id=fight, round_nr=round.round_number, attacker=round.attacker, defender=round.defender, damage=round.damage, previous_hp=round.previous_hp, current_hp=round.current_hp)

	@staticmethod
	def find_fighters_by_params(params):
		predicates = []
		for key, value in params:
			if key not in FightClubDbService.fighter_parameters_map:
				raise AttributeError(f"Parameter {key} is unknown for Fighter object."
					f" Following attributes are allowed: {', '.join(FightClubDbService.fighter_parameters_map)}")
			if key is not None and value is not None:
				predicates.append((FightClubDbService.fighter_parameters_map[key]==value))
		query = (Round.select())
		if len(predicates):
			query = (query.where(reduce(operator.and_, predicates)))
		return list(query)

	@staticmethod
	def find_fights_by_params(params):
		predicates = []
		for key, value in params:
			if key not in FightClubDbService.fight_parameters_map:
				raise AttributeError(f"Parameter {key} is unknown for Fight object."
					f" Following attributes are allowed: {', '.join(FightClubDbService.fight_parameters_map)}")
			if key is not None and value is not None:
				predicates.append((FightClubDbService.fight_parameters_map[key]==value))
		query = (Round.select())
		if len(predicates):
			query = (query.where(reduce(operator.and_, predicates)))
		return list(query)

	@staticmethod
	def find_rounds_by_params(params):
		predicates = []
		for key, value in params:
			if key not in FightClubDbService.round_parameters_map:
				raise AttributeError(f"Parameter {key} is unknown for Round object."
					f" Following attributes are allowed: {', '.join(FightClubDbService.round_parameters_map)}")
			if key is not None and value is not None:
				predicates.append((FightClubDbService.round_parameters_map[key]==value))
		query = (Round.select())
		if len(predicates):
			query = (query.where(reduce(operator.and_, predicates)))
		return list(query)



