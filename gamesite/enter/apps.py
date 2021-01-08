from django.apps import AppConfig


class EnterConfig(AppConfig):
    name = 'enter'

    def ready(self):
        from .signals import match_result
