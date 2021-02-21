from django.apps import AppConfig


class EnterConfig(AppConfig):
    name = 'enter'

    def ready(self):
        from .signals import match_result, updated_called_bets, removed_from_called_bets, label_entries, relabel_entries
