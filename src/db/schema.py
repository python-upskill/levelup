from peewee import *

db = SqliteDatabase('../../combat.db')


class Combatant(Model):
    id = PrimaryKeyField()
    name = CharField()
    hit_points = IntegerField()
    damage_pattern = CharField()

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


def create_tables():
    for e in [Combatant, Battle, Round]:
        if not e.table_exists():
            e.create_table()


create_tables()
