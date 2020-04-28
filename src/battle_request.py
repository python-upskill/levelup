from conbatant_repository import CombatantRepository


class BattleRequest:
    combatants = []
    max_rounds: int

    def __init__(self, combatants: list, max_rounds: int):

        for name in combatants:
            self.combatants.append(CombatantRepository.get(name))
        self.max_rounds = max_rounds
