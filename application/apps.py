from django.apps import AppConfig


class ApplicationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'application'

    def ready(self):
        import sys
        sys.path.append("C:/Users/User/Desktop/Python/BlogDjango/project/application/signals")
        # import signals.signal_handlers
