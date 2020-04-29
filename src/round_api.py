import json, falcon, jsonpickle
from fight_club_db_service import FightClubDbService

class RoundApi:
    def on_get(self, req, resp):
        try:
            rounds = FightClubDbService.find_rounds_by_params(req.params.items())
            resp.content_type = 'application/json'
            resp.body = jsonpickle.encode(rounds, unpicklable=False)
        except AttributeError as err:
            resp.status = falcon.HTTP_400
            resp.body = json.dumps({'error': [err.args]}) 
            return