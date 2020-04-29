import arena
import database
import dnd5eapi
from json import JSONEncoder
from wsgiref import simple_server
import json
import falcon


def read_combatant(combatant_name: str) -> arena.Combatant:
    combatant: arena.Combatant = database.read_combatant(combatant_name)
    if combatant is None:
        combatant = dnd5eapi.read_combatant(combatant_name)
        database.write_combatant(combatant)
    return combatant


class ArenaResource:

    def on_post(self, req, resp):
        resp.status = falcon.HTTP_200
        battle_result: arena.Arena.BattleResult = arena.Arena(
            read_combatant("orc"),
            read_combatant("orc"), 10).fight()
        database.write_battle_result(battle_result)
        resp.body = json.dumps(battle_result, cls=self.BattleResultEncoder)

    class BattleResultEncoder(JSONEncoder):
        def default(self, o):
            return o.__dict__


app = falcon.API()
app.add_route('/fight', ArenaResource())

if __name__ == "__main__":
    database.setup()
    httpd = simple_server.make_server('127.0.0.1', 7011, app)
    httpd.serve_forever()
