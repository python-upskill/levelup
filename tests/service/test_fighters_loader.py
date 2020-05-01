import json
from dataclasses import dataclass
from unittest import TestCase, mock
from unittest.mock import patch

from dto.fighter_dto import FighterDto
from repository.fighter_repository import FighterRepository
from service.fighters_loader import FightersLoader


@dataclass
class JsonResponse:
    payload: dict
    status: int

    def json(self):
        return self.payload


def mocked_fighter_repository_find_fighter_by_index(*args, **kwargs):
    if args[0] == "chimera":
        m = mock.Mock()
        m.name = "Chimera"
        return m
    else:
        return None


def mocked_fighter_repository_save_fighter(*args, **kwargs):
    return None


def mocked_request_get(*args, **kwargs):
    if args[0] == "https://www.dnd5eapi.co/api/monsters/orc":
        orc_data = {
            "name": "Orc",
            "hit_points": 15,
            "actions": [{"damage": [{"damage_dice": "1d12", "damage_bonus": 3}]}],
        }
        return JsonResponse(orc_data, 200)
    elif args[0] == "https://www.dnd5eapi.co/api/monsters/invalid":
        orc_data = {
            "name": "Invalid",
            "hit_points": 15,
            "actions": [{"damage": [{"damage_bonus": 3}]}],
        }
        return JsonResponse(orc_data, 200)
    else:
        return JsonResponse({"error": "Not found"}, 404)


class TestFightClubService(TestCase):
    @mock.patch(
        "repository.fighter_repository.FighterRepository.find_fighter_by_index",
        side_effect=mocked_fighter_repository_find_fighter_by_index,
    )
    @mock.patch(
        "repository.fighter_repository.FighterRepository.save_fighter",
        side_effect=mocked_fighter_repository_save_fighter,
    )
    @mock.patch("requests.get", side_effect=mocked_request_get)
    def test_loading_data(self, mock_fighter_find, mock_fighter_save, mock_request_get):
        fighters = FightersLoader.load_fighters(["orc", "chimera"])
        assert fighters[0].name == "Orc"
        assert fighters[1].name == "Chimera"

    @mock.patch(
        "repository.fighter_repository.FighterRepository.find_fighter_by_index",
        side_effect=mocked_fighter_repository_find_fighter_by_index,
    )
    @mock.patch(
        "repository.fighter_repository.FighterRepository.save_fighter",
        side_effect=mocked_fighter_repository_save_fighter,
    )
    @mock.patch("requests.get", side_effect=mocked_request_get)
    def test_loading_exception_for_monster_not_found(
        self, mock_fighter_find, mock_fighter_save, mock_request_get
    ):
        try:
            fighters = FightersLoader.load_fighters(["unknown", "chimera"])
        except AttributeError:
            assert True
        else:
            assert False

    @mock.patch(
        "repository.fighter_repository.FighterRepository.find_fighter_by_index",
        side_effect=mocked_fighter_repository_find_fighter_by_index,
    )
    @mock.patch(
        "repository.fighter_repository.FighterRepository.save_fighter",
        side_effect=mocked_fighter_repository_save_fighter,
    )
    @mock.patch("requests.get", side_effect=mocked_request_get)
    def test_loading_exception_for_monster_without_damage_defined(
        self, mock_fighter_find, mock_fighter_save, mock_request_get
    ):
        try:
            fighters = FightersLoader.load_fighters(["invalid", "chimera"])
        except AttributeError:
            assert True
        else:
            assert False
