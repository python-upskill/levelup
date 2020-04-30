import json

from api.rest_api import RestApi
from repository.fight_repository import FightRepository
from service.fight_club_service import FightClubService
from service.fighters_loader import FightersLoader


class FightApi(RestApi):
    def on_post(self, req, resp):
        data = json.loads(req.stream.read())
        try:
            fighters = FightersLoader.load_fighters(data["combatants"])
        except AttributeError as err:
            self._bad_request_error_response(resp, err)
            return
        fight_result = FightClubService().fight(fighters, int(data["max_rounds"]))
        FightRepository.save_fight_result(fight_result)
        self._correct_response(resp, fight_result)

    def on_get(self, req, resp):
        try:
            fights = FightRepository.find_fights_by_params(req.params.items())
            self._correct_response(resp, fights)
        except AttributeError as err:
            self._bad_request_error_response(resp, err)
