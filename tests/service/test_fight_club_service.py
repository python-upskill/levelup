from random import randint
from unittest import TestCase

from dto.fighter_dto import FighterDto
from service.fight_club_service import FightClubService


class TestFightClubService(TestCase):
    fight_club = None

    @classmethod
    def setup_class(cls):
        cls.fight_club = FightClubService()

    def test_fight(self):
        for __index in range(100):
            round_max_number = randint(1, 10)
            fighter1_damage = f"{randint(1, 5)}d{randint(1, 10)}"
            fighter2_damage = f"{randint(1, 5)}d{randint(1, 10)}"
            fighter1 = FighterDto(
                "fighter1", randint(20, 200), fighter1_damage, randint(0, 5)
            )
            fighter2 = FighterDto(
                "fighter2", randint(20, 200), fighter2_damage, randint(0, 5)
            )
            fighters = [fighter1, fighter2]
            self.verify_fight_result(fighters, round_max_number)

    def verify_fight_result(self, fighters: list, round_max_number):
        fighters_map = {fighters[0].name: fighters[0], fighters[1].name: fighters[1]}
        result = self.fight_club.fight(fighters, round_max_number)

        assert (
            result.victory.rounds_number >= 1
            and result.victory.rounds_number <= round_max_number
        )

        next_attacker = None
        next_defender = None
        for round in result.rounds:
            attacker = fighters_map[round.attacker]
            defender = fighters_map[round.defender]
            next_attacker = defender
            next_defender = attacker
            attacker_damage_factors = attacker.damage_dice.split("d")
            attacker_damage_multiplier = int(attacker_damage_factors[0])
            attacker_damage_range = int(attacker_damage_factors[1])

            assert round.attacker != round.defender
            assert (
                round.damage >= attacker_damage_multiplier * 1 + attacker.damage_bonus
                and round.damage
                <= attacker_damage_multiplier * attacker_damage_range
                + attacker.damage_bonus
            )

        """assert result.victory.winner_name == "fighter1" or result.victory.winner_name == "fighter2"
		assert result.victory.ko == False
		assert len(result.rounds) == result.victory.rounds_number
		last_round = result.rounds[result.victory.rounds_number - 1]
		assert last_round.round_number == result.victory.rounds_number
		assert last_round.attacker == result.victory.winner_name
		if result.victory.winner_name == "fighter1":
			assert last_round.defender == "fighter2"
			assert last_round.damage >= 2 * 1 + 2 and last_round.damage <= 2 * 5 + 2
		else:
			assert last_round.defender == "fighter1"
			assert last_round.damage >= 1 * 1 + 5 and last_round.damage <= 1 * 5 + 5"""
