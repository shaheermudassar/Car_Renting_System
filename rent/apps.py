from django.apps import AppConfig


class RentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'rent'

    # this function starts the background schedulers defined in schedulers module
    def ready(self):
        from schedulars import updater
        updater.start()