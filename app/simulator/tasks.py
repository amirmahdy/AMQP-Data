import pika
import environ
from celery import shared_task
from celery.signals import celeryd_init
import random
from threading import Thread
from simulator.services import ToCSV
import time

env = environ.Env(
    DEBUG=(bool, False),
    SENTRY=(bool, False),
)


def singleton(class_):
    instances = {}

    def get_instance(*args, **kwargs):
        if "Instance" not in instances:
            instances["Instance"] = class_(*args, **kwargs)
        return instances["Instance"]

    return get_instance


@singleton
class RabbitListener:
    def __init__(self):
        print("back_listener *** 15540")
        self.connection = None
        self.channel = None
        self.try_connection()

    def try_connection(self):
        try:
            crd = pika.PlainCredentials(username=env("RABBIT_USER"), password=env("RABBIT_PASS"))
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(host="rabbitmq", port=5672, credentials=crd))
            self.channel = self.connection.channel()
            self.channel.queue_declare(queue="simulator")
        except Exception as e:
            time.sleep(5)

    def back_listener(self):
        while self.channel is None:
            try:
                self.try_connection()
            except Exception as e:
                time.sleep(5)

        # to_csv = ToCSV()
        def callback(ch, method, properties, body):
            # to_csv.write_to_csv(body.decode())
            print("%r" % body.decode())

        self.channel.basic_consume(
            queue="simulator", on_message_callback=callback, auto_ack=True
        )
        self.channel.start_consuming()

    def back_listener_instance(self):
        t1 = Thread(target=self.back_listener)
        t1.start()

    def send_random_data(self):
        rnd = random.randint(0, 9000)
        self.channel.basic_publish(exchange='', routing_key='simulator', body=str(rnd).encode())


@celeryd_init.connect
def back_listener(conf=None, **kwargs):
    rl = RabbitListener()
    rl.back_listener_instance()


@shared_task(name='random_data')
def random_data():
    rl = RabbitListener()
    rl.send_random_data()
