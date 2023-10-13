from django.apps import AppConfig

#
class SolarConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'solar'

    def ready(self):
        from .signals import create_profile, save_profile
