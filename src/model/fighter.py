from peewee import *

db = SqliteDatabase("fight_club2.db", pragmas={"journal_mode": "wal"})


class Fighter(Model):
    id = PrimaryKeyField(null=False)
    index = CharField(unique=True)
    name = CharField(unique=True)
    hp = IntegerField()
    damage_dice = CharField()
    damage_bonus = IntegerField()

    class Meta:
        database = db
        db_table = "fighter"


def create_table():
    with db:
        db.create_tables([Fighter])


create_table()
