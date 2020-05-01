import json
from dataclasses import dataclass
from unittest import TestCase, mock
from unittest.mock import patch

import falcon
import jsonpickle

from api.fighter_api import FighterApi
from api_test import *
from dto.fighter_dto import FighterDto

fighters_filtered_list_result = {
    "id": 2,
    "index": "orc",
    "name": "Orc",
    "hp": 15,
    "damage_dice": "1d12",
    "damage_bonus": 3,
}


def mocked_fighter_repository_find_fighters_by_params(*args, **kwargs):
    if args[0] == {"name": "Orc"}:
        return fighters_filtered_list_result
    else:
        raise AttributeError("Unknown filter parameter")


class TestFighterApi(TestCase):
    @mock.patch(
        "repository.fighter_repository.FighterRepository.find_fighters_by_params",
        side_effect=mocked_fighter_repository_find_fighters_by_params,
    )
    def test_find_fighter(self, mock_fighter_repository):
        req = HttpRequest(HttpRequestParams({"name": "Orc"}))
        resp = JsonResponse(None, None, None)

        fighter_api = FighterApi()
        fighter_api.on_get(req, resp)

        assert resp.content_type == "application/json"
        assert resp.status == falcon.HTTP_200
        assert resp.body == jsonpickle.encode(
            fighters_filtered_list_result, unpicklable=False
        )

    @mock.patch(
        "repository.fighter_repository.FighterRepository.find_fighters_by_params",
        side_effect=mocked_fighter_repository_find_fighters_by_params,
    )
    def test_find_fighter_wrong_parameter(self, mock_fighter_repository):
        req = HttpRequest(HttpRequestParams({"nameee": "Orc"}))
        resp = JsonResponse(None, None, None)

        fighter_api = FighterApi()
        fighter_api.on_get(req, resp)

        assert resp.content_type == "application/json"
        assert resp.status == falcon.HTTP_400
