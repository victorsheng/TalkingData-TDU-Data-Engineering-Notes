import json
import logging
from  time import sleep

from pyspark import SparkContext
from pyspark.streaming import StreamingContext


logging_format = '%(asctime)s - %(message)s'
logging.basicConfig(format=logging_format)
logger = logging.getLogger('data_stream_test')
logger.setLevel(logging.DEBUG)


data_stream_module=__import__('data_stream')


test_input = [
    json.dumps({'Timestamp': '1559307450.05',
                 'Symbol': 'BTC-USDC','LastTradePrice': '100.0'}),
    json.dumps({'Timestamp': '1559307450.05',
                'Symbol': 'BTC-USDC', 'LastTradePrice': '200.0'}),
    json.dumps({'Timestamp': '1559307450.05',
                'Symbol': 'BTC-USDC', 'LastTradePrice': '300.0'})
]
topic = 'test_topic'

class TestKafkaProducer():
        def __init__(self):
            self.target_topic=None
            self.value=None

        def send(self,target_topic,value):
            self.target_topic = target_topic
            self.value=value

        def log(self):
            print 'taget_topic: %s ,value: %s '% (self.target_topic,self.value)

def _make_dstream_helper(sc, ssc, input):
    input_rdds = [sc.parallelize(test_input, 1)]
    input_stream = ssc.queueStream(input_rdds)
    return input_stream

def _isclose(a,b,rel_tol=1e-09,abs_tol=0.0):
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)


def test_data_stream(sc,ssc,topic):
    input_stream=_make_dstream_helper(sc,ssc,test_input)

    kafkaProducer=TestKafkaProducer()
    data_stream_module.process_stream(input_stream,kafkaProducer,topic)

    ssc.start()
    sleep(5)
    ssc.stop
    
    assert _isclose( json.loads(kafkaProducer.value)['Average'], 200.0)

    print 'test_data_stream passed!!'



if __name__ == "__main__":
    sc=SparkContext('local[2]','local-testing')
    ssc =StreamingContext(sc,1)

    test_data_stream(sc,ssc,topic)
