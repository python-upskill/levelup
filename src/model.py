from peewee import *

db = SqliteDatabase('fight_club2.db', pragmas={'journal_mode': 'wal'})

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

class Fight(Model):
	id = PrimaryKeyField(null=False)
	winner = CharField()
	rounds_number = IntegerField()
	ko =  BooleanField()
	class Meta:
		database = db
		db_table = "fight"

class Round(Model):
	id = PrimaryKeyField(null=False)
	fight_id = ForeignKeyField(Fight, backref='rounds')
	round_nr = IntegerField()
	attacker = CharField()
	defender = CharField()
	damage = IntegerField()
	previous_hp = IntegerField()
	current_hp = IntegerField()
	class Meta:
		database = db
		db_table = "round"

def create_tables():
    with db:
        db.create_tables([Fighter, Round, Fight])
create_tables()

