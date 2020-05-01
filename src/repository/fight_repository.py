import operator
from functools import reduce

from dto.fight_result_dto import FightResultDto
from model.fight import Fight
from model.round import Round


class FightRepository:
    @staticmethod
    def save_fight_result(fight_result: "FightResultDto"):
        fight = Fight.create(
            winner=fight_result.victory.winner_name,
            rounds_number=fight_result.victory.rounds_number,
            ko=fight_result.victory.ko,
        )
        for round in fight_result.rounds:
            Round.create(
                fight_id=fight,
                round_nr=round.round_number,
                attacker=round.attacker,
                defender=round.defender,
                damage=round.damage,
                previous_hp=round.previous_hp,
                current_hp=round.current_hp,
            )

    @staticmethod
    def find_fights_by_params(params):
        predicates = []
        for key, value in params:
            if key not in Fight._meta.fields.keys():
                raise AttributeError(
                    f"Parameter {key} is unknown for Fight object."
                    f" Following attributes are allowed: "
                    f"{', '.join(Fight._meta.fields.keys())}"
                )
            if key is not None and value is not None:
                predicates.append((getattr(Fight, key) == value))
        query = Fight.select()
        if len(predicates):
            query = query.where(reduce(operator.and_, predicates))
        return list(query)
