from unittest import mock

from falcon import testing

import application
import arena
import database


def to_battle_result(response_json: dict) -> arena.BattleResult:
    battle_result = arena.BattleResult(
        victory=to_battle_result_victory(response_json["victory"]),
        rounds=[
            to_battle_result_round(battle_result_round_json)
            for battle_result_round_json in response_json["rounds"]
        ],
    )
    return battle_result


def to_battle_result_victory(
    battle_result_victory_json: dict,
) -> arena.BattleResult.Victory:
    return arena.BattleResult.Victory(**battle_result_victory_json)


def to_battle_result_round(battle_result_round_json: dict) -> arena.BattleResult.Round:
    return arena.BattleResult.Round(**battle_result_round_json)


def mocked_dnd5eapi_read_combatant(*args, **kwargs):
    if args[0] == "orc":
        return arena.Combatant("orc", 100, "1d2")
    if args[0] == "orc2":
        return arena.Combatant("orc2", 110, "3d4 + 5")
    else:
        raise AttributeError(f"Mock for combatant {args[0]} not found!")


class FalconTestCase(testing.TestCase):
    def setUp(self):
        super(FalconTestCase, self).setUp()
        self.app = application.create()


class TestApplication(FalconTestCase):
    @mock.patch("dnd5eapi.read_combatant", side_effect=mocked_dnd5eapi_read_combatant)
    def test_arena(self, mock_requests):
        arena.random.randint = lambda a, b: 1
        database.tear_down()
        database.setup()

        battle_result = to_battle_result(
            self.simulate_post(
                path="/arena", json={"max_rounds": 1, "combatants": ["orc", "orc2"]}
            ).json
        )

        self.assertEqual(
            battle_result,
            arena.BattleResult(
                victory=arena.BattleResult.Victory(winner="orc2", rounds=1, ko=False),
                rounds=[
                    arena.BattleResult.Round(
                        round_number=1,
                        attacker="orc",
                        defender="orc2",
                        damage=1,
                        previous_hp=110,
                        current_hp=109,
                    )
                ],
            ),
        )

    @mock.patch("dnd5eapi.read_combatant", side_effect=mocked_dnd5eapi_read_combatant)
    def test_battle_results(self, mock_requests):
        arena.random.randint = lambda a, b: 1
        database.tear_down()
        database.setup()

        battle_result_1 = to_battle_result(
            self.simulate_post(
                path="/arena", json={"max_rounds": 1, "combatants": ["orc", "orc2"]}
            ).json
        )

        battle_result_2 = to_battle_result(
            self.simulate_post(
                path="/arena", json={"max_rounds": 2, "combatants": ["orc2", "orc"]}
            ).json
        )

        battle_results_json = self.simulate_get(
            path="/battle_results", params={"limit": 2}
        ).json
        battle_results = [
            to_battle_result(battle_result_json)
            for battle_result_json in battle_results_json
        ]

        self.assertEqual([battle_result_2, battle_result_1], battle_results)
