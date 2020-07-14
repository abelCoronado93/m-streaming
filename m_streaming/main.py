import sys

from pyspark.sql import SparkSession
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils

from m_streaming.common.data_functions import DataFunction

if __name__ == "__main__":
    sc = SparkSession.builder.appName("StructuredNetworkWordCount").getOrCreate()
    ssc = StreamingContext(sc.sparkContext, 5)

    brokers, topic = sys.argv[1:]
    kvs = KafkaUtils.createDirectStream(ssc, [topic], {"metadata.broker.list": brokers})
    lines = kvs \
        .map(lambda x: x[1]) \
        .map(lambda x: DataFunction.load_json_from_string(x))

    lines.pprint()

    ssc.start()
    ssc.awaitTermination()
