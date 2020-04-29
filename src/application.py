import arena
import database
import dnd5eapi
from json import JSONEncoder
from wsgiref import simple_server
import json
import falcon
from typing import List
from dataclasses import dataclass


def read_combatant(combatant_name: str) -> arena.Combatant:
    combatant: arena.Combatant = database.read_combatant(combatant_name)
    if combatant is None:
        combatant = dnd5eapi.read_combatant(combatant_name)
        database.write_combatant(combatant)
    return combatant


class ArenaResource:

    def on_post(self, req, resp):
        fight_request = self.FightRequest(**req.media)
        battle_result: arena.Arena.BattleResult = arena.Arena(
            read_combatant(fight_request.combatants[0]),
            read_combatant(fight_request.combatants[1]), fight_request.max_rounds).fight()
        database.write_battle_result(battle_result)
        resp.status = falcon.HTTP_200
        resp.body = json.dumps(battle_result, cls=self.BattleResultEncoder)

    class BattleResultEncoder(JSONEncoder):
        def default(self, o):
            return o.__dict__

    @dataclass
    class FightRequest:
        max_rounds: int
        combatants: List[str]


def create():
    database.setup()
    app = falcon.API()
    app.add_route('/arena', ArenaResource())
    return app


if __name__ == "__main__":
    httpd = simple_server.make_server('127.0.0.1', 7011, create())
    httpd.serve_forever()
