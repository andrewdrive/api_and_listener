import json
from time import sleep
from logging import log
from kafka import KafkaProducer


def on_send_success(record_metadata):
    print('On_send_success_callback', 'topic= ', record_metadata.topic,
                                      'partition= ', record_metadata.partition,
                                      'offset= ', record_metadata.offset)


def on_send_error(exc):
    log.error('I am an errback', exc_info=exc)


sleep(2)
producer = KafkaProducer(bootstrap_servers=['kafka:9092'], value_serializer=lambda m: json.dumps(m).encode('utf-8'))


