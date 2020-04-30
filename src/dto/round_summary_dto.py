from dataclasses import dataclass


@dataclass
class RoundSummaryDto:
    round_number: int
    attacker: str
    defender: str
    damage: int
    previous_hp: int
    current_hp: int
