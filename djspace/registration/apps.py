from django.apps import AppConfig


class RegistrationConfig(AppConfig):
    name = 'djspace.registration'
    verbose_name = 'Registration Application'

    def ready(self):
        import djspace.registration.signals
