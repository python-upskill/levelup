import falcon
from peewee import *

from api.fight_api import FightApi
from api.fighter_api import FighterApi
from api.round_api import RoundApi
from model.fight import Fight
from model.fighter import Fighter
from model.round import Round

WORKS = True

"""def initialize_db():
    db = SqliteDatabase('fight_club2.db', pragmas={'journal_mode': 'wal'})
    with db:
        db.create_tables([Fighter, Round, Fight])

class BaseModel(Model):
    class Meta:
        database = db

initialize_db()"""

api = falcon.API()

api.add_route("/fight", FightApi())
api.add_route("/fighter", FighterApi())
api.add_route("/round", RoundApi())
