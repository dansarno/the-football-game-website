from django.apps import AppConfig


class EnterConfig(AppConfig):
    name = 'enter'

    def ready(self):
        from .signals import updated_called_bets, removed_from_called_bets, recalculate_after_entry_removal, label_entries, relabel_entries
