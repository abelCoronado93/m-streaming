import sys

from pyspark import SparkContext
from pyspark.sql.types import StructField, StructType, StringType
from pyspark.sql import Row

from pyspark.sql import SparkSession
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
from pyspark.sql.context import SQLContext

from m_streaming.common.data_functions import DataFunction

if __name__ == "__main__":
    sc = SparkContext("local", "Broadcast app")
    spark = SparkSession.builder.appName("StreamingLogProcessor").getOrCreate()
    ssc = StreamingContext(sc, 5)

    brokers, topic = sys.argv[1:]
    kvs = KafkaUtils.createDirectStream(ssc, [topic], {"metadata.broker.list": brokers})

    fields = ['hola']
    bc = sc.broadcast(fields).value

    schema = StructType([
        StructField(field, StringType(), True) for field in fields
    ])

    lines = kvs \
        .map(lambda x: x[1]) \
        .flatMap(lambda x: DataFunction.parse_str_to_list(x, bc))

    lines.pprint()
    rdd = lines.foreachRDD(lambda x: x)

    df = SQLContext.createDataFrame(rdd, schema)
    # df.show(10)

    ssc.start()
    ssc.awaitTermination()
