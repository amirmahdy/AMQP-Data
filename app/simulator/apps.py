from django.apps import AppConfig
from threading import Thread
from simulator.tasks import back_listener


class SimulatorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'simulator'

    def ready(self):
        t1 = Thread(target=back_listener)
        t1.start()
