from peewee import *
from dataclasses import dataclass

db = SqliteDatabase('../../combat.db')


@dataclass
class Combatant(Model):
    id = PrimaryKeyField()
    name = TextField()
    hit_points = IntegerField()
    damage_pattern = TextField()

    class Meta:
        database = db
        db_table = 'combatants'


class Battle(Model):
    id = PrimaryKeyField()
    winner_id = ForeignKeyField(Combatant)
    ko = BooleanField(default=0)

    class Meta:
        database = db
        db_table = 'battles'


class Round(Model):
    id = PrimaryKeyField()
    round_number = IntegerField()
    battle_id = ForeignKeyField(Battle)
    attacker_id = ForeignKeyField(Combatant)
    opponent_id = ForeignKeyField(Combatant)
    damage = IntegerField()
    opponent_hp_before_attack = IntegerField()
    opponent_hp_after_attack = IntegerField()

    class Meta:
        database = db
        db_table = 'rounds'


class CombatantState(Model):
    id = ForeignKeyField(Combatant)
    hp_before_attack = IntegerField()
    hp_after_attack = IntegerField()

    class Meta:
        database = db
        db_table = 'combatant_states'


def create_tables():
    for e in [Combatant, Battle, Round, CombatantState]:
        if not e.table_exists():
            e.create_table()


create_tables()
