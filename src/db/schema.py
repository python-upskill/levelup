import os
from peewee import *

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
db = SqliteDatabase(ROOT_PATH + '/../../combat.db')


class CombatantEntity(Model):
    id = PrimaryKeyField()
    name = TextField()
    hit_points = IntegerField()
    damage_pattern = TextField()

    class Meta:
        database = db
        db_table = 'combatants'


class BattleEntity(Model):
    id = PrimaryKeyField()
    winner_id = ForeignKeyField(model=CombatantEntity, null=True)
    ko = BooleanField(default=0)
    max_rounds = IntegerField(null=True)

    class Meta:
        database = db
        db_table = 'battles'


class RoundEntity(Model):
    id = PrimaryKeyField()
    round_number = IntegerField()
    battle_id = ForeignKeyField(BattleEntity)
    attacker_id = ForeignKeyField(CombatantEntity)
    opponent_id = ForeignKeyField(CombatantEntity)

    class Meta:
        database = db
        db_table = 'rounds'


class DefenderStateEntity(Model):
    round_id = ForeignKeyField(RoundEntity)
    hp_before_attack = IntegerField()
    hp_after_attack = IntegerField()

    class Meta:
        database = db
        db_table = 'defender_states'
        primary_key = CompositeKey('round_id')


def create_tables():
    for e in [CombatantEntity, BattleEntity, RoundEntity, DefenderStateEntity]:
        if not e.table_exists():
            e.create_table()


create_tables()