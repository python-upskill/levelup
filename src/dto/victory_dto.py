from dataclasses import dataclass


@dataclass
class VictoryDto:
    winner_name: str
    rounds_number: int
    ko: bool
