from unittest import TestCase

import arena


class TestCombatant(TestCase):

    def test_damage_parsing_success(self):
        damage1 = arena.Combatant.Damage("1d2")
        self.assertEqual(damage1._Damage__dice_roll_number, 1)
        self.assertEqual(damage1._Damage__dice_sides_number, 2)
        self.assertEqual(damage1._Damage__attack_bonus, 0)

        damage2 = arena.Combatant.Damage("1d2 + 3")
        self.assertEqual(damage2._Damage__dice_roll_number, 1)
        self.assertEqual(damage2._Damage__dice_sides_number, 2)
        self.assertEqual(damage2._Damage__attack_bonus, 3)

    def test_damage_drawing(self):
        arena.random.randint = lambda a, b: 2
        self.assertEqual(arena.Combatant.Damage("1d2 + 3").draw(), 5)

    def test_combatant_damage(self):
        combatant1 = arena.Combatant("a", 100, "1d2")
        self.assertEqual("1d2", combatant1.damage())

        combatant2 = arena.Combatant("a", 100, "1d2 + 3")
        self.assertEqual("1d2 + 3", combatant2.damage())

    def test_combatant_attack(self):
        arena.random.randint = lambda a, b: 3

        attacker = arena.Combatant("a", 100, "1d2")
        defender = arena.Combatant("b", 5, "1d2")

        self.assertEqual(5, defender.last_health)
        self.assertEqual(5, defender.health)
        self.assertFalse(defender.is_dead())

        attacker.attack(defender)
        self.assertEqual(3, attacker.last_damage)
        self.assertEqual(5, defender.last_health)
        self.assertEqual(2, defender.health)
        self.assertFalse(defender.is_dead())

        attacker.attack(defender)
        self.assertEqual(3, attacker.last_damage)
        self.assertEqual(2, defender.last_health)
        self.assertEqual(0, defender.health)
        self.assertTrue(defender.is_dead())


class TestArena(TestCase):

    def test_fight(self):
        arena.random.randint = lambda a, b: 3
        battle_result_1: arena.Arena.BattleResult = arena.Arena(
            arena.Combatant("a", 100, "1d2"),
            arena.Combatant("b", 5, "1d2"),
            1).fight()

        victory_1: arena.Arena.BattleResult.Victory = battle_result_1.victory
        self.assertEqual("a", victory_1.winner)
        self.assertEqual(1, victory_1.rounds)
        self.assertFalse(victory_1.ko)

        self.assertEqual(1, len(battle_result_1.rounds))
        round_1: arena.Arena.BattleResult.Round = battle_result_1.rounds[0]
        self.assertEqual(1, round_1.round_number)
        self.assertEqual("a", round_1.attacker)
        self.assertEqual("b", round_1.defender)
        self.assertEqual(5, round_1.previous_hp)
        self.assertEqual(2, round_1.current_hp)
