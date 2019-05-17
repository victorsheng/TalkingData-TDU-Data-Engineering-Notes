import argparse
from kafka import KafkaConsumer

def consume(topic_name, kafka_borker):
    consumer = KafkaConsumer(topic_name, bootstrap_servers=kafka_borker)

    for message in consumer:
        print message

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('topic_name', help='the kafka topic push to.')
    parser.add_argument('kafka_borker', help='the location of the kafka broker')

    args = parser.parse_args()
    topic_name = args.topic_name
    kafka_borker = args.kafka_borker

    consume(topic_name, kafka_borker)

