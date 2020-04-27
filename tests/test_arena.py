import arena
from unittest import TestCase


class TestDamage(TestCase):

    def test_damage_parsing_success(self):
        damage1 = arena.Damage("1d2")
        self.assertTrue(damage1._Damage__x == 1)
        self.assertTrue(damage1._Damage__y == 2)
        self.assertTrue(damage1._Damage__z == 0)

        damage2 = arena.Damage("1d2 + 3")
        self.assertTrue(damage2._Damage__x == 1)
        self.assertTrue(damage2._Damage__y == 2)
        self.assertTrue(damage2._Damage__z == 3)
        pass

    def test_damage_drawing(self):
        damage = arena.Damage("1d2 + 3")
        self.assertTrue(damage.draw() > 0)
        pass


class TestCombatant(TestCase):

    def test_combatant(self):
        combatant = arena.Combatant("c", 100, arena.Damage("1d2"))
        self.assertFalse(combatant.is_dead())

        last_damage = combatant.attack()
        self.assertTrue(last_damage == combatant.last_damage)

        last_health = combatant.health
        self.assertTrue(combatant.get_attacked(100) == 0)
        self.assertTrue(last_health == combatant.last_health)