from django.apps import AppConfig
from .signals import signal_init

class WriterHomeAppConfig(AppConfig):
    name = 'writerhome'

    def ready(self):
        super(WriterHomeAppConfig, self).ready()
        #print("Inside ready function, before signal_init")
        signal_init()
        #print("Inside ready function, after signal_init")
