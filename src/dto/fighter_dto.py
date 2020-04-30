from dataclasses import dataclass


@dataclass
class FighterDto:
    name: str
    hp: int
    damage_dice: str
    damage_bonus: int
