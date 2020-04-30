from peewee import *

db = SqliteDatabase("fight_club2.db", pragmas={"journal_mode": "wal"})


class Fight(Model):
    id = PrimaryKeyField(null=False)
    winner = CharField()
    rounds_number = IntegerField()
    ko = BooleanField()

    class Meta:
        database = db
        db_table = "fight"


def create_table():
    with db:
        db.create_tables([Fight])


create_table()
