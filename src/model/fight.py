from peewee import (
    BooleanField,
    CharField,
    IntegerField,
    Model,
    PrimaryKeyField,
    SqliteDatabase,
)

db = SqliteDatabase("fight_club.db", pragmas={"journal_mode": "wal"})


class Fight(Model):
    id = PrimaryKeyField(null=False)
    winner = CharField()
    rounds_number = IntegerField()
    ko = BooleanField()

    class Meta:
        database = db
        db_table = "fight"


def create_table() -> None:
    with db:
        db.create_tables([Fight])


create_table()
