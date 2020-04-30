from db.schema import *
from abc import ABC
import peewee


class Query(ABC):

    def find_by_query(self, query: peewee.ModelSelect) -> list:
        return list(query)


class CombatantQuery(Query):

    def find_by_name(self, name: str) -> CombatantEntity:
        return self.find_by_query(CombatantEntity.select().where(CombatantEntity.name.contains(name)));
