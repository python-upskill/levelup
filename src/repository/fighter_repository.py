import operator
from functools import reduce

from model.fighter import Fighter


class FighterRepository:
    @staticmethod
    def find_fighter_by_index(index: str) -> "Fighter":
        fighter = Fighter.get_or_none(Fighter.index == index)
        return fighter

    @staticmethod
    def save_fighter(fighter_index: str, dto: "FighterDto"):
        Fighter.create(index=fighter_index, **dataclasses.asdict(dto))

    @staticmethod
    def find_fighters_by_params(params):
        predicates = []
        for key, value in params:
            if key not in Fighter._meta.fields.keys():
                raise AttributeError(
                    f"Parameter {key} is unknown for Fighter object."
                    f" Following attributes are allowed: {', '.join(Fighter._meta.fields.keys())}"
                )
            if key is not None and value is not None:
                predicates.append((getattr(Fighter, key) == value))
        query = Fighter.select()
        if len(predicates):
            query = query.where(reduce(operator.and_, predicates))
        return list(query)
