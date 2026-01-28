from django.apps import AppConfig


class EstructuraacademicaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'EstructuraAcademica'
    def ready(self):
        import EstructuraAcademica.signals