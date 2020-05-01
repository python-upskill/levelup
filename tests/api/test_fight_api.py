import json
from unittest import TestCase, mock
from unittest.mock import patch

import falcon
import jsonpickle

from api.fight_api import FightApi
from api_test import *
from dto.fighter_dto import FighterDto

fight_result = {
    "rounds": [
        {
            "round_number": 1,
            "attacker": "Orc",
            "defender": "Chimera",
            "damage": 14,
            "previous_hp": 114,
            "current_hp": 100,
        }
    ],
    "victory": {"winner_name": "Chimera", "rounds_number": 1, "ko": "false"},
}

fight_filtered_list_result = {
    "id": 2,
    "winner": "Chimera",
    "rounds_number": 2,
    "ko": "true",
}


def mocked_fighters_loader_load_fighters(*args, **kwargs):
    if args[0] == ["chimera", "orc"]:
        return [FighterDto("Chimera", 100, "1d5", 2), FighterDto("Orc", 15, "2d4", 3)]
    else:
        raise AttributeError("Fighter not found")


def mocked_fight_club_service_fight(*args, **kwargs):
    if (
        args[0]
        == [FighterDto("Chimera", 100, "1d5", 2), FighterDto("Orc", 15, "2d4", 3)]
        and args[1] == 7
    ):
        return fight_result
    else:
        raise AttributeError(
            "Fight club service invoked with unexpected arguments for fight method"
        )


def mocked_fight_repository_save_fight_result(*args, **kwargs):
    if args[0] == fight_result:
        return None
    else:
        raise AttributeError(
            "Fight repository invoked with unexpected arguments for save method"
        )


def mocked_fight_repository_find_fights_by_params(*args, **kwargs):
    if args[0] == {"rounds_number": 2}:
        return fight_filtered_list_result
    else:
        raise AttributeError("Unknown filter parameter")


class TestFightApi(TestCase):
    @mock.patch(
        "service.fighters_loader.FightersLoader.load_fighters",
        side_effect=mocked_fighters_loader_load_fighters,
    )
    @mock.patch(
        "service.fight_club_service.FightClubService.fight",
        side_effect=mocked_fight_club_service_fight,
    )
    @mock.patch(
        "repository.fight_repository.FightRepository.save_fight_result",
        side_effect=mocked_fight_repository_save_fight_result,
    )
    def test_positive_scenario(
        self, mock_fight_repository, mock_fight_club_service, mock_fighters_loader
    ):
        req = JsonRequest(
            JsonRequestStream('{"combatants": ["chimera", "orc"], "max_rounds": 7}')
        )
        resp = JsonResponse(None, None, None)

        fight_api = FightApi()
        fight_api.on_post(req, resp)

        assert resp.content_type == "application/json"
        assert resp.status == falcon.HTTP_200
        assert resp.body == jsonpickle.encode(fight_result, unpicklable=False)
        mock_fighters_loader.assert_called_once_with(["chimera", "orc"])
        mock_fight_club_service.assert_called_once_with(
            [FighterDto("Chimera", 100, "1d5", 2), FighterDto("Orc", 15, "2d4", 3)], 7
        )
        mock_fight_repository.assert_called_once_with(fight_result)

    @mock.patch(
        "service.fighters_loader.FightersLoader.load_fighters",
        side_effect=mocked_fighters_loader_load_fighters,
    )
    @mock.patch(
        "service.fight_club_service.FightClubService.fight",
        side_effect=mocked_fight_club_service_fight,
    )
    @mock.patch(
        "repository.fight_repository.FightRepository.save_fight_result",
        side_effect=mocked_fight_repository_save_fight_result,
    )
    def test_fighter_not_found(
        self, mock_fight_repository, mock_fight_club_service, mock_fighters_loader
    ):
        req = JsonRequest(
            JsonRequestStream('{"combatants": ["chimera", "unknown"], "max_rounds": 7}')
        )
        resp = JsonResponse(None, None, None)

        fight_api = FightApi()
        fight_api.on_post(req, resp)

        assert resp.content_type == "application/json"
        assert resp.status == falcon.HTTP_400
        mock_fighters_loader.assert_called_once_with(["chimera", "unknown"])
        mock_fight_club_service.assert_not_called()
        mock_fight_repository.assert_not_called()

    @mock.patch(
        "repository.fight_repository.FightRepository.find_fights_by_params",
        side_effect=mocked_fight_repository_find_fights_by_params,
    )
    def test_find_fight(self, mock_fight_repository):
        req = HttpRequest(HttpRequestParams({"rounds_number": 2}))
        resp = JsonResponse(None, None, None)

        fight_api = FightApi()
        fight_api.on_get(req, resp)

        assert resp.content_type == "application/json"
        assert resp.status == falcon.HTTP_200
        assert resp.body == jsonpickle.encode(
            fight_filtered_list_result, unpicklable=False
        )

    @mock.patch(
        "repository.fight_repository.FightRepository.find_fights_by_params",
        side_effect=mocked_fight_repository_find_fights_by_params,
    )
    def test_find_fight_wrong_parameter(self, mock_fight_repository):
        req = HttpRequest(HttpRequestParams({"rounds_number_ddd": 2}))
        resp = JsonResponse(None, None, None)

        fight_api = FightApi()
        fight_api.on_get(req, resp)

        assert resp.content_type == "application/json"
        assert resp.status == falcon.HTTP_400
