from __future__ import print_function

import json
from pymongo import MongoClient
from influxdb import InfluxDBClient


class DataFunction:

    def __init__(self, config: dict):
        self._config = config

    def create_df(self, spark, sql_context, rdd):
        df = spark.read.json(rdd)
        df.registerTempTable('logs')
        ret = sql_context.sql('select * from logs').toJSON().take(self._config['max_batch_size'])
        [self._send_record_influx(json.loads(i)) for i in ret]

    @staticmethod
    def _send_record_mongo(data: json):
        connection = MongoClient()
        db = connection.get_database('m_streaming')
        co = db.get_collection('apache_logs')

        co.insert_one(json.loads(data))

        connection.close()

    def _send_record_influx(self, data: json):
        client = InfluxDBClient('localhost', '8086', 'superadmin', 'eskere', 'tmp')

        input_fields = self._config['input_fields']
        json_body = [
            {
                'measurement': 'apache_logs',
                'tags': {
                    'host': data['host'],
                    'user': data['user'],
                    'method': data['method'],
                    'code': data['code']
                },
                'fields': {
                    'size': data['size']
                }
            }
        ]

        client.write_points(json_body)

        client.close()

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
