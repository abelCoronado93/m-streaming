from __future__ import print_function

import json

from pymongo import MongoClient


class DataFunction(object):

    @staticmethod
    def create_df(spark, sql_context, rdd):
        df = spark.read.json(rdd)
        df.registerTempTable("logs")
        ret = sql_context.sql(sqlQuery="SELECT * FROM logs").toJSON().take(100)
        [DataFunction.send_record(i) for i in ret]

    @staticmethod
    def send_record(data: json):
        connection = MongoClient()
        db = connection.get_database("m_streaming")
        co = db.get_collection("apache_logs")

        co.insert_one(json.loads(data))

        connection.close()

    @staticmethod
    def load_json_from_string(json_str: str) -> dict:
        try:
            ret = json.loads(json_str)
        except json.JSONDecodeError:
            ret = dict()

        return ret

    @staticmethod
    def parse_str_to_list(json_data: json, fields) -> list:
        try:
            return [tuple(json_data.get(field) for field in fields)]
        except json.JSONDecodeError:
            return []
