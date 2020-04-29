from unittest import TestCase

import arena
import database


class TestCombatantModel(TestCase):

    def test_write_read(self):
        database.tear_down()
        database.setup()
        combatant1 = arena.Combatant("a", 100, "1d2")
        database.write_combatant(combatant1)
        combatant2 = database.read_combatant(combatant1.name)
        self.assertIsNotNone(combatant2)
        self.assertEqual(combatant1.name, combatant2.name)
        self.assertEqual(combatant1.health, combatant2.health)
        self.assertEqual(combatant1.damage(), combatant2.damage())
