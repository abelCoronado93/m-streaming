import sys
import traceback
import yaml

from pyspark.sql import SparkSession, SQLContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils

from m_streaming.common.data_functions import DataFunction


if __name__ == "__main__":

    try:
        with open(sys.argv[1], 'r') as yml:
            config = yaml.load(yml)
    except FileNotFoundError as ex:
        print('ERROR: Config file does not exist: ' + str(ex) + '\n')
        traceback.print_tb(ex.__traceback__)

    print(config)

    spark = SparkSession \
        .builder \
        .appName(config['app_name']) \
        .getOrCreate()
    ssc = StreamingContext(spark.sparkContext, config['batch_window'])
    sql_context = SQLContext(spark)

    kvs = KafkaUtils.createDirectStream(ssc,
                                        [config['kafka_topic']],
                                        {"metadata.broker.list": config['kafka_brokers']})

    data_functions = DataFunction(config)

    lines = kvs \
        .map(lambda rdd: rdd[1]) \
        .map(data_functions.load_json_from_string) \
        .filter(lambda x: x != {})

    lines.foreachRDD(lambda rdd: data_functions.create_df(spark, sql_context, rdd))

    ssc.start()
    ssc.awaitTermination()
