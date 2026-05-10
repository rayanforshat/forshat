from django.apps import AppConfig


class FormsAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'forms_app'
    verbose_name = 'مبادرة العلاج'

    def ready(self):
        import forms_app.signals  # noqa: F401
