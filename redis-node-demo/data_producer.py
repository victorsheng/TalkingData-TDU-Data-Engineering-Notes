import argparse
import atexit
import logging
import schedule
import time
import requests
import json

from kafka import KafkaProducer
from kafka.errors import KafkaError, KafkaTimeoutError

logging_format='%(asctime)s - %(message)s'
logging.basicConfig(format=logging_format)
logger = logging.getLogger('data_producer')
logger.setLevel(logging.DEBUG)

API_BASE = 'https://api.pro.coinbase.com'
requests.DEFAULT_RETRIES = 5

def check_symbol(symbol):
    '''
    helper method to check if the symbol exists in coinbase API
    '''
    logger.debug('Checking symbol.')
    try:
        response = requests.get(API_BASE+'/products')
        products_ids= [product['id'] for product in response.json()]

        if symbol not in products_ids:
            logger.warn('Symbol %s not supported. The list of supported symbols : %s ',symbol,products_ids)
            exit();
    except Exception as e:
            logger.warn('Failed to fetch products. %s',e.message)
            exit();

def fetch_price(symbol, producer, topic_name):
    logger.debug('start to fetch price for %s',symbol)
    try:
        response = requests.get('%s/products/%s/ticker'%(API_BASE, symbol))
        price =response.json()['price']
        timestamp=time.time()
        payload ={'Symbol':str(symbol),
                'LastTradePrice':str(price),
                'Timestamp':str(timestamp)
                }
        logger.debug('Retrived %s info %s',symbol, payload)
        producer.send(topic=topic_name, value=json.dumps(payload),timestamp_ms=int(time.time()*1000))

    except KafkaTimeoutError as timeout_error:
        logger.warn('Failed to send messages to kafka, casued by :%s',timeout_error.message)
    except Exception as e:
        logger.warn('Failed to fetch price: %s', e)


def shutdown_hook(producer):
    try:
        producer.flush(10)
    except KafakaError as kafka_error:
        logger.warn('Failed to flush pending messages, caused by %s',kafka_error.message)
    finally:
        try:
            producer.close(10)
        except Exception as e:
            logger.warn('FIaled to close kafka connection, caused by %s',e.message)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('symbol',help='the symbol you want to pull.')
    parser.add_argument('topic_name',help='the kafka topic push to.')
    parser.add_argument('kafka_borker',help='the location of the kafka broker')


    # Parse arguments
    args=parser.parse_args()
    symbol=args.symbol
    topic_name=args.topic_name
    kafka_borker=args.kafka_borker

    # check if the symbol is supported
    check_symbol(symbol);

    # instantiate a simple kafka producer
    producer = KafkaProducer(bootstrap_servers=kafka_borker)

    # Schedule and run the fetch price function every second
    schedule.every(1).second.do(fetch_price, symbol, producer, topic_name)

    # Setup proper shutdown hook
    atexit.register(shutdown_hook, producer)

    while True:
        schedule.run_pending()
