import falcon
import json
from util.json_operations import toJSON
from arena import JsonArena
from combatants.retriever import CombatantNotFoundException


class CombatantResource:

    def on_post(self, req: falcon.Request, resp: falcon.Response):
        raw_data = json.load(req.bounded_stream)
        arena = JsonArena(max_rounds=int(raw_data['max_rounds']))
        try:
            arena.init_by_names(raw_data['combatants'])
        except CombatantNotFoundException as e:
            resp.body = toJSON({'error': str(e)})
            resp.status = falcon.HTTP_400
            return
        arena.start_battle()
        resp.body = arena.get_summary()
        resp.status = falcon.HTTP_200


api = falcon.API()
api.add_route('/battle', CombatantResource())