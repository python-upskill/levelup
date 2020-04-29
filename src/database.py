from peewee import *
import datetime
import arena

db = SqliteDatabase('my_database.db')


class BaseModel(Model):
    class Meta:
        database = db


class CombatantModel(BaseModel):
    name = CharField(unique=True)
    health = IntegerField()
    damage = CharField()


class BattleModel(BaseModel):
    winner = ForeignKeyField(CombatantModel, backref='namex') # if I change this to 'name' it breaks
    rounds = IntegerField()
    ko = BooleanField()
    created_date = DateTimeField(default=datetime.datetime.now)


def setup():
    if db.is_closed():
        db.connect()
    db.create_tables([CombatantModel])


def tear_down():
    if db.is_closed():
        db.connect()
    db.drop_tables([CombatantModel])


def write_combatant(combatant: arena.Combatant):
    CombatantModel.create(name=combatant.name,
                          health=combatant.health,
                          damage=combatant.damage())


def read_combatant(combatant_name: str) -> arena.Combatant:
    combatant: CombatantModel = CombatantModel.select().where(CombatantModel.name == combatant_name)
    if combatant is not None:
        return arena.Combatant(combatant.name, combatant.health, combatant.damage)
    else:
        return None


def write_battle_result(battle_result: arena.Arena.BattleResult):
    BattleModel.create(winner=battle_result.Victory.winner,
                       rounds=len(battle_result.rounds),
                       ko=battle_result.Victory.ko,
                       created_date=datetime.datetime.now())
