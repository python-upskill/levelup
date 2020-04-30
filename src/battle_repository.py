from dataclasses import asdict
from battle_result import *
from db.entities import *


class BattleRepository:

    @classmethod
    def save_battle(cls, battle: BattleResult):
        battle_entity: BattleEntity = BattleEntity(**asdict(battle.victory))
        battle_entity.save(force_insert=True)

        battle_round: RoundResult

        for battle_round in battle.rounds:
            battle_round_dict = asdict(battle_round)
            round_entity: RoundEntity = RoundEntity(battle_id=battle_entity.id, **battle_round_dict)
            round_entity.save(force_insert=True)

    @classmethod
    def find_all(cls) -> [BattleResult]:
        battles = BattleEntity.select().order_by(BattleEntity.created_at.desc())

        result = [BattleResult]
        for battle in battles:
            battle_result = BattleResult()
            victory: Victory = Victory(winner=battle.winner.name, round=battle.round, ko=battle.ko)
            battle_result.victory = victory
            battle_rounds: [RoundEntity] = RoundEntity.select() \
                .where(RoundEntity.battle_id == battle.id) \
                .order_by(RoundEntity.round_number)
            for round in battle_rounds:
                round_result: RoundResult = RoundResult(round_number=round.round_number,
                                                        attacker=round.attacker.name,
                                                        defender=round.defender.name,
                                                        damage=round.damage,
                                                        previous_hp=round.previous_hp,
                                                        current_hp=round.current_hp)
                battle_result.rounds.append(round_result)
            result.append(battle_result)

        return result
