from arena import *
from battle_request import *
from battle_repository import *
import falcon
import json


class ArenaResource(object):

    def on_post(self, req, resp):
        try:
            battle_request: BattleRequest = self.__parse_request(req)
        except ValueError as err:
            resp.status = falcon.HTTP_400
            resp.body = json.dumps({'error': err.args})
            return

        arena = Arena(battle_request)
        battle_result: BattleResult = arena.fight()
        BattleRepository.save_battle(battle_result)

        resp.status = falcon.HTTP_200
        resp.body = battle_result.to_json()

    def __parse_request(self, req) -> BattleRequest:
        data = json.loads(req.stream.read())
        combatants = data['combatants']
        max_rounds = int(data['max_rounds'])
        return BattleRequest(combatants, max_rounds)


class BattleResource(object):

    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.body = jsonpickle.encode(BattleRepository.find_all(),
                                      unpicklable=False)


app = falcon.API()

app.add_route("/arena/fight", ArenaResource())
app.add_route("/battle", BattleResource())
