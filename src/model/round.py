from peewee import *

from model.fight import Fight

db = SqliteDatabase("fight_club2.db", pragmas={"journal_mode": "wal"})


class Round(Model):
    id = PrimaryKeyField(null=False)
    fight_id = ForeignKeyField(Fight, backref="rounds")
    round_nr = IntegerField()
    attacker = CharField()
    defender = CharField()
    damage = IntegerField()
    previous_hp = IntegerField()
    current_hp = IntegerField()

    class Meta:
        database = db
        db_table = "round"


def create_table():
    with db:
        db.create_tables([Round])


create_table()
