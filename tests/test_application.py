from falcon import testing

import application
import arena


def to_battle_result(response_json: dict) -> arena.BattleResult:
    battle_result = arena.BattleResult(
        victory=to_battle_result_victory(response_json["victory"]),
        rounds=[to_battle_result_round(battle_result_round_json) for battle_result_round_json in
                response_json["rounds"]])
    return battle_result


def to_battle_result_victory(battle_result_victory_json: dict) -> arena.BattleResult.Victory:
    return arena.BattleResult.Victory(**battle_result_victory_json)


def to_battle_result_round(battle_result_round_json: dict) -> arena.BattleResult.Round:
    return arena.BattleResult.Round(**battle_result_round_json)


class FalconTestCase(testing.TestCase):
    def setUp(self):
        super(FalconTestCase, self).setUp()
        self.app = application.create()


class TestApplication(FalconTestCase):

    def test_application(self):
        battle_result = to_battle_result(self.simulate_post(path="/arena",
                                                            json={
                                                                'max_rounds': 2,
                                                                'combatants': ["orc", "ancient-gold-dragon"]
                                                            }).json)
        print(battle_result)
