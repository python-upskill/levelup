import datetime
from typing import List

from peewee import *

import arena

db = SqliteDatabase('my_database.db')


class BaseModel(Model):
    class Meta:
        database = db


class CombatantModel(BaseModel):
    name = CharField(unique=True)
    health = IntegerField()
    damage = CharField()

    def from_combatant(self,
                       combatant: arena.Combatant) -> 'CombatantModel':
        return self.create(name=combatant.name,
                           health=combatant.health,
                           damage=combatant.damage)

    def to_combatant(self):
        return arena.Combatant(self.name, self.health, self.damage)


class BattleResultModel(BaseModel):
    created_date = DateTimeField(default=datetime.datetime.now)
    winner = ForeignKeyField(CombatantModel, backref='victories')
    rounds = IntegerField()
    ko = BooleanField()

    def from_battle_result(self,
                           battle_result: arena.BattleResult,
                           combatant_model_winner: CombatantModel) -> 'BattleResultModel':
        return self.create(
            created_date=datetime.datetime.now(),
            rounds=battle_result.victory.rounds,
            winner=combatant_model_winner,
            ko=battle_result.victory.ko)

    def to_battle_result(self, battle_result_round_models: 'BattleResultRoundModels') -> arena.BattleResult:
        return arena.BattleResult(victory=arena.BattleResult.Victory(
            rounds=self.rounds,
            winner=self.winner.name,
            ko=self.ko),
            rounds=[battle_result_round_model.to_battle_result_round()
                    for battle_result_round_model in battle_result_round_models])


class BattleResultRoundModel(BaseModel):
    battle = ForeignKeyField(BattleResultModel, backref='battles')
    attacker = ForeignKeyField(CombatantModel, field='name', backref='attacks')
    defender = ForeignKeyField(CombatantModel, field='name', backref='defenses')
    round_number = IntegerField()
    damage = IntegerField()
    previous_hp = IntegerField()
    current_hp = IntegerField()

    class Meta:
        indexes = (
            (('battle_id', 'round_number'), True),
        )

    def from_battle_result_round(self,
                                 battle_result_round: arena.BattleResult.Round,
                                 battle_result_model: BattleResultModel,
                                 combatant_model_attacker: CombatantModel,
                                 combatant_model_defender: CombatantModel) -> 'BattleResultRoundModel':
        return self.create(
            battle=battle_result_model,
            attacker=combatant_model_attacker,
            defender=combatant_model_defender,
            round_number=battle_result_round.round_number,
            damage=battle_result_round.damage,
            previous_hp=battle_result_round.previous_hp,
            current_hp=battle_result_round.current_hp)

    def to_battle_result_round(self) -> arena.BattleResult.Round:
        return arena.BattleResult.Round(
            round_number=self.round_number,
            attacker=self.attacker.name,
            defender=self.defender.name,
            damage=self.damage,
            previous_hp=self.previous_hp,
            current_hp=self.current_hp)


BattleResultRoundModels = List[BattleResultRoundModel]


def setup():
    if db.is_closed():
        db.connect()
    db.create_tables([CombatantModel, BattleResultModel, BattleResultRoundModel])


def tear_down():
    if db.is_closed():
        db.connect()
    db.drop_tables([CombatantModel, BattleResultModel, BattleResultRoundModel])


def write_combatant(combatant: arena.Combatant):
    CombatantModel().from_combatant(combatant)


def read_combatant(combatant_name: str) -> arena.Combatant:
    combatant_model: CombatantModel = CombatantModel.get_or_none(CombatantModel.name == combatant_name)
    if combatant_model is not None:
        return combatant_model.to_combatant()
    else:
        return None


def write_battle_result(battle_result: arena.BattleResult):
    combatant_models: dict = {
        battle_result.rounds[0].attacker: CombatantModel.get(CombatantModel.name == battle_result.rounds[0].attacker),
        battle_result.rounds[0].defender: CombatantModel.get(CombatantModel.name == battle_result.rounds[0].defender),
    }
    battle_result_model = BattleResultModel().from_battle_result(battle_result,
                                                                 combatant_models.get(battle_result.victory.winner))
    for battle_result_round in battle_result.rounds:
        BattleResultRoundModel().from_battle_result_round(battle_result_round,
                                                          battle_result_model,
                                                          combatant_models.get(battle_result_round.attacker),
                                                          combatant_models.get(battle_result_round.defender))


def read_battle_result_latest() -> arena.BattleResult:
    battle_result_model: BattleResultModel = BattleResultModel.select()\
        .order_by(BattleResultModel.created_date.desc()).get()
    battle_result_round_models: BattleResultRoundModels = BattleResultRoundModel.select() \
        .where(BattleResultRoundModel.battle == battle_result_model)
    return battle_result_model.to_battle_result(battle_result_round_models)
