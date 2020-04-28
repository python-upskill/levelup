import falcon
import json
from arena import JsonArena


class Resource(object):

    def on_get(self, req, resp):
        arena = JsonArena()
        arena.init()
        arena.start_battle()
        resp.body = arena.get_summary()
        resp.status = falcon.HTTP_200

    def on_post(self, req: falcon.Request, resp: falcon.Response):
        raw_data = json.load(req.bounded_stream)
        max_rounds = int(raw_data['max_rounds'])
        print(raw_data['combatants'][0])


api = falcon.API()
api.add_route('/battle', Resource())

    # arena = JsonArena()
    # arena.init()
    # arena.start_battle()
    # print(arena.get_summary())