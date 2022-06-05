import json
from time import sleep
from logging import log
from kafka import KafkaProducer
from kafka.errors import KafkaError


def on_send_success(record_metadata):
    print(record_metadata.topic)
    print(record_metadata.partition)
    print(record_metadata.offset)


def on_send_error(exc):
    log.error('I am an errback', exc_info=exc)


sleep(2)
producer = KafkaProducer(bootstrap_servers=['kafka:9092'], value_serializer=lambda m: json.dumps(m).encode('ascii'))


