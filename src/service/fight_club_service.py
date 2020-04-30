from random import randint

from dto.fight_result_dto import FightResultDto
from dto.round_summary_dto import RoundSummaryDto
from dto.victory_dto import VictoryDto


class FightClubService:
    def __calculate_damage_dice(self, damage_dice_pattern):
        damage_factors = damage_dice_pattern.split("d")
        multiplier = int(damage_factors[0])
        damage_range = int(damage_factors[1])
        damage = 0
        for __index in range(multiplier):
            damage += randint(1, damage_range)
        return damage

    def __calculate_damage(self, fighter):
        damage = (
            self.__calculate_damage_dice(fighter.damage_dice) + fighter.damage_bonus
        )
        return damage

    def __sum_up_fight(self, fighters, round_number):
        fighters = sorted(fighters, key=lambda fighter: fighter.hp)
        winner = fighters[-1]
        loser = fighters[0]
        ko = loser.hp <= 0
        return VictoryDto(winner.name, round_number, ko)

    def __draw_fighters_slots(self, fighters):
        first_fighter = fighters[randint(0, 1)]
        fighters.remove(first_fighter)
        second_fighter = fighters[0]
        fighters_with_drawed_slots = [first_fighter, second_fighter]
        return fighters_with_drawed_slots

    def fight(self, fighters_list: list, max_rounds_number: int) -> "FightResultDto":
        print(fighters_list)
        round_number = 0
        rounds_summary_list = []
        fighters = self.__draw_fighters_slots(fighters_list)
        while all(f.hp > 0 for f in fighters) and round_number < max_rounds_number:
            round_number += 1
            attacker = fighters[round_number % 2]
            defender = fighters[(round_number + 1) % 2]
            damage = self.__calculate_damage(attacker)
            defender_previous_hp = defender.hp
            defender.hp = defender_previous_hp - damage
            round_summary = RoundSummaryDto(
                round_number,
                attacker.name,
                defender.name,
                damage,
                defender_previous_hp,
                defender.hp,
            )
            rounds_summary_list.append(round_summary)
        victory = self.__sum_up_fight(fighters, round_number)
        result = FightResultDto(rounds_summary_list, victory)
        print(result)
        return result
