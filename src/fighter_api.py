import json, falcon, jsonpickle
from fight_club_db_service import FightClubDbService

class FighterApi:
    def on_get(self, req, resp):
        try:
            fighters = FightClubDbService.find_fighters_by_params(req.params.items())
            resp.content_type = 'application/json'
            resp.body = jsonpickle.encode(fighters, unpicklable=False)
        except AttributeError as err:
            resp.status = falcon.HTTP_400
            resp.body = json.dumps({'error': [err.args]}) 
            return