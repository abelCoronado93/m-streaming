from __future__ import print_function
import json


class DataFunction(object):

    @staticmethod
    def load_json_from_string(json_str: str) -> dict:
        try:
            ret = json.loads(json_str)
        except json.JSONDecodeError:
            ret = dict()

        return ret
