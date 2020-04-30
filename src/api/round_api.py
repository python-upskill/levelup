import json

from api.rest_api import RestApi
from repository.round_repository import RoundRepository


class RoundApi(RestApi):
    def on_get(self, req, resp):
        try:
            rounds = RoundRepository.find_rounds_by_params(req.params.items())
            self._correct_response(resp, rounds)
        except AttributeError as err:
            self._bad_request_error_response(resp, err)
            return
