#!/bin/bash

start-master.sh
start-slave.sh spark://abel-PORTEGE-R930:7077

sh ${KAFKA_HOME}/bin/zookeeper-server-start.sh ${KAFKA_HOME}/config/zookeeper.properties &
sh ${KAFKA_HOME}/bin/kafka-server-start.sh ${KAFKA_HOME}/config/server.properties &

sh ${KAFKA_HOME}/bin/kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic test
