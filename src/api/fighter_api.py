import json

from api.rest_api import RestApi
from repository.fighter_repository import FighterRepository


class FighterApi(RestApi):
    def on_get(self, req, resp):
        try:
            fighters = FighterRepository.find_fighters_by_params(req.params.items())
            self._correct_response(resp, fighters)
        except AttributeError as err:
            self._bad_request_error_response(resp, err)
            return
