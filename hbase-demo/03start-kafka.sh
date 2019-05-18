docker run -d -p 9092:9092 -e KAFKA_ZOOKEEPER_CONNECT=hbase-vic:2181 -e KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://localhost:9092  --name kafka-hbase-vic --net network-hb confluentinc/cp-kafka

