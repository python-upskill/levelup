from unittest import TestCase

import arena
import database


class TestCombatantModel(TestCase):

    def test_combatant_write_read(self):
        database.tear_down()
        database.setup()

        combatant_1 = arena.Combatant("a", 100, "1d2")
        database.write_combatant(combatant_1)

        combatant_2 = database.read_combatant(combatant_1.name)
        self.assertIsNotNone(combatant_2)
        self.assertEqual(combatant_1.name, combatant_2.name)
        self.assertEqual(combatant_1.health, combatant_2.health)
        self.assertEqual(combatant_1.damage, combatant_2.damage)

        combatant3 = database.read_combatant("x")
        self.assertIsNone(combatant3)


class TestBattleResultModel(TestCase):

    def test_battle_result_write_read(self):
        database.tear_down()
        database.setup()

        combatant_1 = arena.Combatant("a", 100, "1d4")
        database.write_combatant(combatant_1)

        combatant_2 = arena.Combatant("b", 100, "1d5")
        database.write_combatant(combatant_2)

        round_1 = arena.BattleResult.Round(round_number=1, attacker="a", defender="b",
                                           damage=4, previous_hp=100, current_hp=96)
        round_2 = arena.BattleResult.Round(round_number=2, attacker="b", defender="a",
                                           damage=5, previous_hp=100, current_hp=95)
        victory = arena.BattleResult.Victory(rounds=2, winner="b", ko=False)
        battle_result_1 = arena.BattleResult(rounds=[round_1, round_2], victory=victory)

        database.write_battle_result(battle_result_1)

        battle_result_2 = database.read_battle_result_latest(1)[0]
        self.assertEqual(battle_result_1, battle_result_2)
