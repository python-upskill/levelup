from peewee import *
import datetime

db = SqliteDatabase('../db/arena.db')


class BaseEntity(Model):
    class Meta:
        database = db


class CombatantEntity(BaseEntity):
    name = CharField(primary_key=True)
    hp = IntegerField()
    damage_pattern = CharField()

    class Meta:
        db_table = 'combatant'


class BattleEntity(BaseEntity):
    id = PrimaryKeyField()
    created_at = DateTimeField(default=datetime.datetime.now)
    winner = ForeignKeyField(CombatantEntity)
    rounds = IntegerField()
    ko = BooleanField()

    class Meta:
        db_table = 'battle'


class RoundEntity(BaseEntity):
    id = PrimaryKeyField()
    round_number = IntegerField()
    battle_id = ForeignKeyField(BattleEntity)
    attacker = ForeignKeyField(CombatantEntity)
    defender = ForeignKeyField(CombatantEntity)
    damage = IntegerField()
    previous_hp = IntegerField()
    current_hp = IntegerField()

    class Meta:
        db_table = 'round'


def create_tables():
    for e in [CombatantEntity, BattleEntity, RoundEntity]:
        if not e.table_exists():
            e.create_table()
