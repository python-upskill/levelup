import json, falcon, jsonpickle
from fighters_loader import FightersLoader
from fight_club import FightClub
from fight_club_db_service import FightClubDbService
from peewee import *

class FightApi:

    def on_post(self, req, resp):
        resp.content_type = 'application/json'
        data = json.loads(req.stream.read())
        fighters_indexes = data['combatants']
        max_rounds_number = int(data['max_rounds'])
        try:
            fighters = self.__load_fighters(fighters_indexes)
        except AttributeError as err:
            resp.status = falcon.HTTP_400
            resp.body = json.dumps({'error': [err.args]}) 
            return
        fight_result = self.__fight(fighters, max_rounds_number)
        FightClubDbService.save_fight_result(fight_result)
        resp.status = falcon.HTTP_200
        resp.body = jsonpickle.encode(fight_result, unpicklable=False)

    def __load_fighters(self, fighters_indexes):
        fighters = []
        for index in fighters_indexes:
            fighter = FightClubDbService.find_fighter_by_index(index)
            if(fighter is None):
                fighter = FightersLoader.load_fighter(index)
                FightClubDbService.save_fighter(index, fighter)
            fighters.append(fighter)
        return fighters

    def __fight(self, fighters, max_rounds_number):
        fight_club = FightClub()
        fight_result = fight_club.fight(fighters, max_rounds_number)
        return fight_result

    def on_get(self, req, resp):
        try:
            fights = FightClubDbService.find_fights_by_params(req.params.items())
            resp.content_type = 'application/json'
            resp.body = jsonpickle.encode(fights, unpicklable=False)
        except AttributeError as err:
            resp.status = falcon.HTTP_400
            resp.body = json.dumps({'error': [err.args]}) 
            return