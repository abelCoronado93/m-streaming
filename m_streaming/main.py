import sys

from pyspark.sql import SparkSession, SQLContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils

from m_streaming.common.data_functions import DataFunction


if __name__ == "__main__":
    spark = SparkSession \
        .builder \
        .appName("StreamingLogProcessor") \
        .getOrCreate()
    ssc = StreamingContext(spark.sparkContext, 5)
    sql_context = SQLContext(spark)

    brokers, topic = sys.argv[1:]
    kvs = KafkaUtils.createDirectStream(ssc, [topic], {"metadata.broker.list": brokers})

    lines = kvs \
        .map(lambda rdd: rdd[1]) \
        .map(DataFunction.load_json_from_string)

    lines.foreachRDD(lambda rdd: DataFunction.create_df(spark, sql_context, rdd))

    ssc.start()
    ssc.awaitTermination()
