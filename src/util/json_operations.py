import json
import requests
from abc import ABC, abstractmethod


class JsonRetriever(ABC):

    def _wrap_with_list(self, obj: object) -> list:
        if type(obj) is list:
            return obj
        return [obj]

    @abstractmethod
    def _retrieve_json(self):
        pass

    def retrieve(self) -> list:
        return self._wrap_with_list(self._retrieve_json())


class FileJsonRetriever(JsonRetriever):
    file_path: str

    def from_path(self, file_path: str) -> 'FileJsonRetriever':
        self.file_path = file_path
        return self

    def _retrieve_json(self):
        with open(self.file_path) as f:
            return json.load(f)


class UrlJsonRetriever(JsonRetriever):
    url: str

    def from_url(self, url: str) -> 'FileJsonRetriever':
        self.url = url
        return self

    def _retrieve_json(self):
        resp = requests.get(self.url)
        if resp.status_code == 200:
            return resp.json()
        msg = f'{self.url} not found'
        raise ResourceNotFoundException(msg)


class ResourceNotFoundException(Exception):
    pass


def toJSON(obj):
    return json.dumps(obj, default=lambda o: o.__dict__,
                      sort_keys=True, indent=4)
