import json
import requests


class JsonRetriever:

    def _wrap_with_list(self, obj: object) -> list:
        if type(obj) is list:
            return obj
        return [obj]

    def from_file(self, path) -> list:
        with open(path) as f:
            return self._wrap_with_list(json.load(f))

    def from_url(self, url) -> list:
        return self._wrap_with_list(json.load(requests.get(url)))


def read_from_file(path):
    with open(path) as f:
        return json.load(f)


def toJSON(obj):
    return json.dumps(obj, default=lambda o: o.__dict__,
                      sort_keys=True, indent=4)
