import json, falcon, jsonpickle
from fighters_loader import FightersLoader
from fight_club import FightClub

WORKS = True

class FightClubApi:

    def on_post(self, req, resp):
        resp.content_type = 'application/json'
        data = json.loads(req.stream.read())
        fighters_names = data['combatants']
        max_rounds_number = int(data['max_rounds'])
        try:
            fighters = self.__load_fighters(fighters_names)
        except AttributeError as err:
            resp.status = falcon.HTTP_400
            resp.body = json.dumps({'error': [err.args]}) 
            return
        fight_result = self.__fight(fighters, max_rounds_number)
        resp.status = falcon.HTTP_200
        resp.body = jsonpickle.encode(fight_result, unpicklable=False)

    def __load_fighters(self, fighters_names):
        fighters = []
        for name in fighters_names:
            fighter = FightersLoader.load_fighter(name)
            fighters.append(fighter)
        return fighters

    def __fight(self, fighters, max_rounds_number):
        fight_club = FightClub()
        fight_result = fight_club.fight(fighters, max_rounds_number)
        return fight_result

api = falcon.API()

api.add_route('/fight', FightClubApi())