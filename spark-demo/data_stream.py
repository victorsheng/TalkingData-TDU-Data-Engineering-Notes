import argparse
import atexit
import logging
import json
from kafka import KafkaProducer
from kafka.errors import KafkaError,KafkaTimeoutError
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
import time

logging_format='%(asctime)s - %(message)s'
logging.basicConfig(format=logging_format)
logger = logging.getLogger('data_stream')
logger.setLevel(logging.DEBUG)

def process_stream(stream,kafka_producer,target_topic):
    
    def send_to_kafka(rdd):
        results=rdd.collect()
        for r in results:
            data=json.dumps({
                'Symbol':r[0],
                'Timestamp':time.time(),
                'Average':r[1]
                })
            try:
                logger.info('Sending average price %s to kafka topic %s',
                            data, target_topic)
                kafka_producer.send(target_topic,value=data)
            except Exception as e:
                logger.warn('Failed to send average price to kafka, casued by :%s',
                            e.message)


    def parir(data):
        record=json.loads(data.decode('utf-8'))
        # (Symbol,(Price, Count))
        return record.get('Symbol'),(float(record.get('LastTradePrice')),1)

    stream.map(parir).reduceByKey(lambda a,b: (a[0]+b[0],a[1]+b[1])).map(lambda (k,v): (k, v[0]/v[1])).foreachRDD(send_to_kafka)


def shutdown_hook(producer):

    try:
        logger.info('Flushing pending message to kafka, timeout is set to 10s')
        producer.flush(10)
        logger.info('Finished flushing pending messages to kafka')
    except KafakaError as kafka_error:
        logger.warn('Failed to flush pending messages, caused by %s',
                    kafka_error.message)
    finally:
        try:
            logger.info('Closing kafka connection')
            producer.close(10)
        except Exception as e:
            logger.warn(
                'Failed to close kafka connection, caused by %s', e.message)



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('source_topic',help='the kafka topic subscribe from.')
    parser.add_argument('target_topic',help='the kafka topic push to.')
    parser.add_argument('kafka_borker',help='the location of the kafka broker')
    parser.add_argument('batch_duration',help='the batch duration in secs')

    args=parser.parse_args()
    source_topic=args.source_topic
    target_topic = args.target_topic
    kafka_borker = args.kafka_borker
    batch_duration = int(args.batch_duration)

    sc = SparkContext('local[2]','AveragePrice')
    sc.setLogLevel("INFO")
    ssc = StreamingContext(sc, batch_duration)
    # create stream 
    directKafkaStream = KafkaUtils.createDirectStream(
        ssc, [source_topic], {'metadata.broker.list': kafka_borker})

    stream=directKafkaStream.map(lambda x: x[1])
    
    kafka_producer=KafkaProducer(bootstrap_servers=kafka_borker)
    # process
    process_stream(stream,kafka_producer,target_topic)

    atexit.register(shutdown_hook, kafka_producer)

    ssc.start()
    ssc.awaitTermination()







    
