from django.apps import AppConfig
from .signals import signal_init

class WriterHomeAppConfig(AppConfig):
    name = 'writerhome'

    def ready(self):
        super(WriterHomeAppConfig, self).ready()
        signal_init()
