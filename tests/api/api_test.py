from dataclasses import dataclass


@dataclass
class HttpRequest:
    params: "HttpRequestParams"


@dataclass
class HttpRequestParams:
    params: dict

    def items(self):
        return self.params


@dataclass
class JsonRequest:
    stream: "JsonRequestStream"


@dataclass
class JsonRequestStream:
    payload: dict

    def read(self):
        return self.payload


@dataclass
class JsonResponse:
    body: dict
    status: int
    content_type: str
