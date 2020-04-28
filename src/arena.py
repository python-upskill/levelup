from report import *
from random import randint


class Arena:
    attacker: Combatant
    opponent: Combatant
    battle_reporter: 'BattleReporter'
    combatants_retriever = FileCombatantRetriever()
    max_rounds: int

    def __init__(self, battle_reporter: 'BattleReporter' = BattleReporter(),
                 max_rounds: int = None):
        self.battle_reporter = battle_reporter
        self.max_rounds = max_rounds

    def retrieve_combatants(self):
        return self.combatants_retriever\
            .from_path('../tasks/combat/combatants.json')\
            .retrieve()

    def init(self):
        combatants = self.retrieve_combatants()
        self.attacker = combatants[randint(0, 1)]
        combatants.remove(self.attacker)
        self.opponent = combatants[0]

    def get_winner(self) -> Combatant:
        if self.attacker.is_lost():
            return self.opponent
        if self.opponent.is_lost():
            return self.attacker
        return None

    def get_current_winner(self) -> Combatant:
        if self.attacker.hp_after_attack >= self.opponent.hp_after_attack:
            return self.attacker
        return self.opponent

    def get_summary(self) -> str:
        return self.battle_reporter.get_summary()

    def is_finished_by_round_nr(self, round_nr: int) -> bool:
        return self.max_rounds and round_nr > self.max_rounds

    def start_battle(self) -> None:
        round_nr = 1
        winner = None
        while not self.is_finished_by_round_nr(round_nr) and not winner:
            self.attacker.attack(self.opponent)
            self.battle_reporter.take_snapshot(self.attacker, self.opponent)
            winner = self.get_winner()
            round_nr += 1
            self.attacker, self.opponent = self.opponent, self.attacker
        if winner:
            self.battle_reporter.finish_battle_by_ko(winner.name)
        else:
            self.battle_reporter.finish_battle(self.get_current_winner().name)


class JsonArena(Arena):
    def __init__(self):
        super(JsonArena, self).__init__(JsonBattleReporter())


if __name__ == "__main__":
    arena = Arena()
    arena.init()
    arena.start_battle()
    print(arena.get_summary())
