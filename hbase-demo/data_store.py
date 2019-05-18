import argparse
import atexit
import happybase
import logging
import json

from kafka import KafkaConsumer
from kafka.errors import KafkaError


logging_format = '%(asctime)s - %(message)s'
logging.basicConfig(format=logging_format)
logger = logging.getLogger('data_storge')
logger.setLevel(logging.DEBUG)

def shutdown_hook(consumer,hbase_connection):
    try:
        logger.info('Closing Kafka consumer.')
        consumer.close()
        logger.info('Kafka consumer closed.')
        logger.info('Closing hbase connection')
        hbase_connection.close()
        logger.info('hbase connection closed')
    except KafkaError as ke:
        logger.warn('Failed to close Kafka consumer, caused by: %s', ke.message)
    finally
        logger.info('Exiting program.')

def persist_data(data,hbase_connection,data_table):
    try:
        logger.debug('Start to persist data to hbase :%s',data)
        parsed =jon.loads(data)
        symbol=parsed.get('Symbol')
        price=float(parsed.get('LastTradePrice'))
        timestamp=parsed.get('Timestamp')

        table=hbase_connection.table(data_table)
        row_key='%s-%s'%(symbol,timestamp)
        logger.info('Storing values with row key:%s',row_key)
        table.put(row_key, {'family:symbol': str(symbol),
                            'family:trade_time':str(timestamp),
                            'family:trade_price':Str(price)})
        logger.debug('Persist data to habse for symbol :%s ,price: %s,timestamp:%s '%s(symbol,price,timestamp))
    
    except Exception as e:
        logger.error('Failed to persist data to habse for %s',e)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('topic_name',help=' kafka topic name to subscribe from.')
    parser.add_argument('kafka_broker',help=' the location of the kafka broker.')
    parser.add_argument('data_table',help=' the datat table to use.')
    parser.add_argument('hbase_host',help=' the host name of hbase.')

    args=parser.parse_args()
    topic_name = args.topic_name
    kafka_broker = args.kafka_broker
    data_table = args.data_table
    hbase_host = args.hbase_host

    consumer =KafkaConsumer(topic_name,bootstrap_servers=kafka_broker)

    hbase_connection=happybase.connection(hbase_host)

    if data_table no in hbase_connection.tables():
        hbase_connection.create_table(data_table,{'faimly':dict()})

    atexit.register(shutdonwn_hook,consumer,hbase_connection)

    for msg in consumer:
        persist_data(msg.value,hbase_connection,data_table)





