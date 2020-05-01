import json
from dataclasses import dataclass
from unittest import TestCase, mock
from unittest.mock import patch

import falcon
import jsonpickle

from api.round_api import RoundApi
from api_test import *
from dto.fighter_dto import FighterDto

rounds_filtered_list_result = {
    "id": 9,
    "fight_id": 3,
    "round_nr": 4,
    "attacker": "Chimera",
    "defender": "Orc",
    "damage": 10,
    "previous_hp": 4,
    "current_hp": -6,
}


def mocked_round_repository_find_rounds_by_params(*args, **kwargs):
    if args[0] == {"round_nr": 4}:
        return rounds_filtered_list_result
    else:
        raise AttributeError("Unknown filter parameter")


class TestFighterApi(TestCase):
    @mock.patch(
        "repository.round_repository.RoundRepository.find_rounds_by_params",
        side_effect=mocked_round_repository_find_rounds_by_params,
    )
    def test_find_round(self, mock_round_repository):
        req = HttpRequest(HttpRequestParams({"round_nr": 4}))
        resp = JsonResponse(None, None, None)

        round_api = RoundApi()
        round_api.on_get(req, resp)

        assert resp.content_type == "application/json"
        assert resp.status == falcon.HTTP_200
        assert resp.body == jsonpickle.encode(
            rounds_filtered_list_result, unpicklable=False
        )

    @mock.patch(
        "repository.round_repository.RoundRepository.find_rounds_by_params",
        side_effect=mocked_round_repository_find_rounds_by_params,
    )
    def test_find_round_wrong_parameter(self, mock_round_repository):
        req = HttpRequest(HttpRequestParams({"round_numberr": 4}))
        resp = JsonResponse(None, None, None)

        round_api = RoundApi()
        round_api.on_get(req, resp)

        assert resp.content_type == "application/json"
        assert resp.status == falcon.HTTP_400
