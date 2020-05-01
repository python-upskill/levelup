from combatants.model import *
from db.query import *
from db.mapper import FromEntityMapper, ToEntityMapper
from util.json_operations import *
from abc import ABC


class CombatantsRetriever(ABC):

    json_retriever: JsonRetriever

    def __init__(self, json_retriever: JsonRetriever):
        self.json_retriever = json_retriever

    def _create_combatants(self, json_elements: list) -> list:
        result = []
        for e in json_elements:
            result.append(Combatant(**e))
        return result

    def _retrieve_json(self) -> list:
        return self.json_retriever.retrieve()

    def _retrieve_from_json(self) -> list:
        return self._create_combatants(self._retrieve_json())

    def retrieve(self) -> list:
        return self._retrieve_from_json()


class FileCombatantRetriever(CombatantsRetriever):

    def __init__(self):
        super(FileCombatantRetriever, self).__init__(FileJsonRetriever())

    def from_path(self, path: str):
        self.json_retriever.from_path(path)
        return self


class UrlCombatantRetriever(CombatantsRetriever):

    def __init__(self):
        super(UrlCombatantRetriever, self).__init__(UrlJsonRetriever())
        self.combatants: list = []

    def _retrieve_json(self) -> list:
        js = super()._retrieve_json()[0]
        data = {'name': js['name'], 'hp': js['hit_points']}
        for action in js['actions']:
            if 'damage' not in action:
                continue
            data['damage'] = action['damage'][0]['damage_dice']
            break
        return [data]

    def _from_url(self, url: str):
        self.json_retriever.from_url(url)
        return self

    def _by_name(self, name: str):
        host = 'https://www.dnd5eapi.co'
        url = f'{host}/api/monsters/?name={name}'
        urls = self.json_retriever.from_url(url).retrieve()
        if urls[0]['count'] == 0:
            msg = f"Combatant named '{name}' not found"
            raise CombatantNotFoundException(msg)
        self._from_url(f"{host}{urls[0]['results'][0]['url']}")
        return self

    def _retrieve_by_name(self) -> list:
        return self._retrieve_from_json()

    def _cache_combatant(self, combatant: Combatant):
        self.combatants.append(combatant)

    def by_names(self, combatant_names: list):
        self.combatants.clear()
        for name in combatant_names[:2]:
            combatant_list = self._by_name(name)._retrieve_by_name()
            self._cache_combatant(combatant_list[0])
        return self

    def retrieve(self) -> list:
        return self.combatants


class DbUrlCombatantRetriever(UrlCombatantRetriever):
    combatants_query: CombatantQuery = CombatantQuery()
    combatants_from_db: list

    def _by_name(self, name: str):
        self.combatants_from_db = self.combatants_query.find_all_by_name(name)
        if not self.combatants_from_db:
            return super()._by_name(name)
        return self

    def _retrieve_by_name(self) -> list:
        if self.combatants_from_db:
            mapper = FromEntityMapper()
            return list(map(lambda c: mapper.map_combatant(c), self.combatants_from_db))
        return super()._retrieve_by_name()

    def _cache_combatant(self, combatant: Combatant):
        filtered = list(filter(lambda c: c.name == combatant.name, self.combatants_from_db))
        if not filtered:
            mapper = ToEntityMapper()
            mapper.map_combatant(combatant).save()
        super()._cache_combatant(combatant)


class CombatantNotFoundException(Exception):
    pass


r = DbUrlCombatantRetriever()
c = r.by_names(['dragon']).retrieve()
pass
