from peewee import (
    CharField,
    ForeignKeyField,
    IntegerField,
    Model,
    PrimaryKeyField,
    SqliteDatabase,
)

from model.fight import Fight

db = SqliteDatabase("fight_club.db", pragmas={"journal_mode": "wal"})


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


def create_table() -> None:
    with db:
        db.create_tables([Round])


create_table()
