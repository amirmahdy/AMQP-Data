import pika
import environ
from celery import shared_task
import random

env = environ.Env(
    DEBUG=(bool, False),
    SENTRY=(bool, False),
)


def back_listener():
    crd = pika.PlainCredentials(username=env("RABBIT_USER"), password=env("RABBIT_PASS"))
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq", port=5672, credentials=crd))
    channel = connection.channel()
    channel.queue_declare(queue="simulator")

    def callback(ch, method, properties, body):
        print("%r" % body.decode())

    channel.basic_consume(
        queue="simulator", on_message_callback=callback, auto_ack=True
    )
    channel.start_consuming()


@shared_task(name='random_data')
def random_data():
    rnd = random.randint(0, 9000)
    crd = pika.PlainCredentials(username=env("RABBIT_USER"), password=env("RABBIT_PASS"))
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq", port=5672, credentials=crd))
    channel = connection.channel()
    channel.queue_declare(queue='simulator')
    channel.basic_publish(exchange='', routing_key='simulator', body=str(rnd).encode())
