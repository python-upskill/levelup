import combatants
from db.schema import *
from abc import ABC
import peewee


class Query(ABC):

    def find_by_query(self, query: peewee.ModelSelect) -> list:
        return list(query)


class CombatantQuery(Query):

    def find_by_name(self, name: str) -> Combatant:
        return self.find_by_query(Combatant.select().where(Combatant.name.contains(name)));
