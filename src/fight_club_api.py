import falcon
from fight_api import FightApi
from fighter_api import FighterApi
from round_api import RoundApi

WORKS = True

api = falcon.API()

api.add_route('/fight', FightApi())
api.add_route('/fighter', FighterApi())
api.add_route('/round', RoundApi())