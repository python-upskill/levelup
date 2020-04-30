from peewee import *

db = SqliteDatabase('../../combat.db')


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
    winner_id = ForeignKeyField(CombatantEntity)
    ko = BooleanField(default=0)

    class Meta:
        database = db
        db_table = 'battles'


class RoundEntity(Model):
    id = PrimaryKeyField()
    round_number = IntegerField()
    battle_id = ForeignKeyField(BattleEntity)
    attacker_id = ForeignKeyField(CombatantEntity)
    opponent_id = ForeignKeyField(CombatantEntity)
    damage = IntegerField()
    opponent_hp_before_attack = IntegerField()
    opponent_hp_after_attack = IntegerField()

    class Meta:
        database = db
        db_table = 'rounds'


class CombatantState(Model):
    id = ForeignKeyField(CombatantEntity)
    hp_before_attack = IntegerField()
    hp_after_attack = IntegerField()

    class Meta:
        database = db
        db_table = 'combatant_states'


def create_tables():
    for e in [CombatantEntity, BattleEntity, RoundEntity, CombatantState]:
        if not e.table_exists():
            e.create_table()


create_tables()
