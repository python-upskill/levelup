import json
from json import JSONEncoder
from typing import List
from wsgiref import simple_server

import falcon
from dataclasses import dataclass

import arena
import database
import dnd5eapi


def read_combatant(combatant_name: str) -> arena.Combatant:
    combatant: arena.Combatant = database.read_combatant(combatant_name)
    if combatant is None:
        combatant = dnd5eapi.read_combatant(combatant_name)
        database.write_combatant(combatant)
    return combatant


class ArenaResource:

    def on_post(self, req, resp):
        fight_request = self.FightRequest(**req.media)
        if fight_request.max_rounds <= 0:
            raise AttributeError(f"max_rounds: {fight_request.max_rounds} <=0!")
        if len(fight_request.combatants) < 2:
            raise AttributeError(f"not enough combatants: {len(fight_request.combatants)}")

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


class BattleResultsResource:

    def on_get(self, req, resp):
        battle_results_request = self.BattleResultsRequest(**req.params)
        if battle_results_request.limit <= 0:
            raise AttributeError(f"limit: {battle_results_request.limit} <=0!")
        if battle_results_request.limit > 100:
            raise AttributeError(f"limit: {battle_results_request.limit} >100!")

        battle_results: arena.Arena.BattleResults = database.read_battle_result_latest(battle_results_request.limit)
        resp.status = falcon.HTTP_200
        resp.body = json.dumps(battle_results, cls=self.BattleResultsEncoder)

    class BattleResultsEncoder(JSONEncoder):
        def default(self, o):
            return o.__dict__

    @dataclass
    class BattleResultsRequest:
        limit: int


def create():
    database.setup()
    app = falcon.API()
    app.add_route('/arena', ArenaResource())
    app.add_route('/battle_results', BattleResultsResource())
    return app


if __name__ == "__main__":
    httpd = simple_server.make_server('127.0.0.1', 7011, create())
    httpd.serve_forever()
