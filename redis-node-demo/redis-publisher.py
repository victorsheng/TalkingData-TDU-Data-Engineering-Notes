import argparse
import atexit
import logging
import redis

from kafka import KafkaConsumer


logging_format = '%(asctime)s - %(message)s'
logging.basicConfig(format=logging_format)
logger = logging.getLogger('redis-pulisher')
logger.setLevel(logging.DEBUG)

def shutdown_hook(kafka_consumer):
    logger.info('Shutdown kafka consumer')
    kafka_consumer.close()


if __name__ == "__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument('topic_name',help='the kafka topic consume from')
    parser.add_argument('kafka_broker')
    parser.add_argument('redis_channel')
    parser.add_argument('redis_host')
    parser.add_argument('redis_port')


    args=parser.parse_args()
    topic_name=args.topic_name
    kafka_broker = args.kafka_broker
    redis_channel = args.redis_channel
    redis_host = args.redis_host
    redis_port = args.redis_port

    kafka_consumer=KafkaConsumer(topic_name,bootstrap_servers=kafka_broker)

    redis_client=redis.StrictRedis(host=redis_host,port=redis_port)

    atexit.register(shutdown_hook,kafka_consumer)

    for msg in kafka_consumer:
        logger.info('Received new datat from kafka :%s' % str(msg))
        redis_client.publish(redis_channel,msg.value)



