import json


class Victory:
    winner: str
    round: int
    ko: bool

    def __init__(self,
                 winner: str,
                 round: int,
                 ko: bool):
        self.winner = winner
        self.round = round
        self.ko = ko


class RoundResult:
    round_number: int
    attacker: str
    defender: str
    damage: int
    previous_hp: int
    current_hp: int

    def __init__(self, round_number: int,
                 attacker: str,
                 defender: str,
                 damage: int,
                 previous_hp: int,
                 current_hp: int):
        self.round_number = round_number
        self.attacker = attacker
        self.defender = defender
        self.damage = damage
        self.previous_hp = previous_hp
        self.current_hp = current_hp


class BattleResult:
    rounds = [2, 3]
    victory: Victory

    def add_round(self, battle_round: RoundResult):
        self.rounds.append(battle_round)

    # FIXME rounds not serialized!!!
    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)
