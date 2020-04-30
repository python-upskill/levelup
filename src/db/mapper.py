import combatants
from db import schema


class FromTableMapper:

    def map_combatant(self, obj: schema.Combatant) -> combatants.Combatant:
        return combatants.Combatant(obj.name, obj.hit_points, obj.damage_pattern)


class ToTableMapper:

    def map_combatant(self, obj: combatants.Combatant) -> schema.Combatant:
        return schema.Combatant(name=obj.name, hit_points=obj.hp_before_attack,
                                damage_pattern=obj.damage_pattern)