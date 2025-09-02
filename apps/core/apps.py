from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.core'
    verbose_name = 'Pinterest Core'
    
    def ready(self):
        # Import signals or other startup code here if needed
        pass