from db.schema import *
from abc import ABC
import peewee


class Query(ABC):

    def find_all_by_query(self, query: peewee.ModelSelect) -> list:
        return list(query)

    def find_first_by_query(self, query: peewee.ModelSelect):
        results = self.find_all_by_query(query)
        if results:
            return results[0]
        return None


class CombatantQuery(Query):

    def find_first_by_name(self, name: str) -> list:
        return self.find_first_by_query(CombatantEntity.select()
                                        .where(CombatantEntity.name == name))

    def find_all_by_name(self, name: str) -> list:
        return self.find_all_by_query(CombatantEntity.select().where(CombatantEntity.name.contains(name)))


class BattleQuery(Query):

    def find_by_id(self, id: int) -> BattleEntity:
        return self.find_first_by_query(BattleEntity.select()
                                        .where(BattleEntity.id == id))


# t = type(CombatantEntity.name.contains('a'))
# pass

# CombatantEntity.create(name='Abel',hit_points=100,damage_pattern='1d2').save()
# CombatantEntity.create(name='Abelard',hit_points=101,damage_pattern='3d2').save()
# CombatantEntity.create(name='Abela',hit_points=102,damage_pattern='3d2').save()
# x = CombatantEntity.create(name='Abela1',hit_points=102,damage_pattern='3d2').save()
# pass

# print(type(CombatantQuery().find_first_by_name('Abela').id))

# class CombatantEntity(Model):
#     id = PrimaryKeyField()
#     name = TextField()
#     hit_points = IntegerField()
#     damage_pattern = TextField()