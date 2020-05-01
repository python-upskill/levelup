import operator
from functools import reduce

from model.round import Round


class RoundRepository:
    @staticmethod
    def find_rounds_by_params(params):
        predicates = []
        for key, value in params:
            if key not in Round._meta.fields.keys():
                raise AttributeError(
                    f"Parameter {key} is unknown for Round object."
                    f" Following attributes are allowed: "
                    f"{', '.join(Round._meta.fields.keys())}"
                )
            if key is not None and value is not None:
                predicates.append((getattr(Round, key) == value))
        query = Round.select()
        if len(predicates):
            query = query.where(reduce(operator.and_, predicates))
        return list(query)
