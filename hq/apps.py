from django.apps import AppConfig


class HqConfig(AppConfig):
    name = 'hq'

    def ready(self):
        from . import signals
    