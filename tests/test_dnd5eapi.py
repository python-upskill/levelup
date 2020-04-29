from unittest import TestCase
from unittest import mock

import dnd5eapi


def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    if args[0] == 'https://www.dnd5eapi.com/api/monsters/orc':
        return MockResponse({'hit_points': 100,
                             'actions': [
                                 {'damage': [
                                     {'damage_dice': '1d2'}
                                 ]}
                             ]}, 200)
    elif args[0] == 'https://www.dnd5eapi.com/api/monsters/orc2':
        return MockResponse({'hit_points': 110,
                             'actions': [
                                 {},
                                 {'damage': [
                                     {},
                                     {
                                         'damage_dice': '2d3',
                                         'damage_bonus': 4
                                     }
                                 ]}
                             ]}, 200)
    return MockResponse(None, 404)


class TestCombatant(TestCase):

    @mock.patch('dnd5eapi.requests.get', side_effect=mocked_requests_get)
    def test_combatant_read(self, mock_get):
        combatant_1 = dnd5eapi.read_combatant('orc')
        self.assertEqual('orc', combatant_1.name)
        self.assertEqual(100, combatant_1.health)
        self.assertEqual('1d2', combatant_1.damage)

        combatant_2 = dnd5eapi.read_combatant('orc2')
        self.assertEqual('orc2', combatant_2.name)
        self.assertEqual(110, combatant_2.health)
        self.assertEqual('2d3 + 4', combatant_2.damage)

        try:
            dnd5eapi.read_combatant('x')
            self.fail()
        except AttributeError as err:
            self.assertEqual("Combatant x not found!", err.args[0])
