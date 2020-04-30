import combatants.model
from db import schema


class FromTableMapper:

    def map_combatant(self, obj: schema.Combatant) -> combatants.model.Combatant:
        return combatants.model.Combatant(obj.name, obj.hit_points, obj.damage_pattern)


class ToTableMapper:

    def map_combatant(self, obj: combatants.model.Combatant) -> schema.Combatant:
        return schema.Combatant(name=obj.name, hit_points=obj.hp_before_attack,
                                damage_pattern=obj.damage_pattern)