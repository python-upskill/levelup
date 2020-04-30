import json

import falcon
import jsonpickle


class RestApi:
    def _bad_request_error_response(self, resp, err):
        resp.content_type = "application/json"
        resp.status = falcon.HTTP_400
        resp.body = json.dumps({"error": [err.args]})

    def _correct_response(self, resp, body_data):
        resp.content_type = "application/json"
        resp.status = falcon.HTTP_200
        resp.body = jsonpickle.encode(body_data, unpicklable=False)
