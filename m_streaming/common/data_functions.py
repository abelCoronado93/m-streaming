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

    @staticmethod
    def parse_str_to_list(json_str: str, fields) -> list:
        try:
            ret = json.loads(json_str)
            return [tuple(ret.get(field) for field in fields)]
        except json.JSONDecodeError:
            return []
