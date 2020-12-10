# -*- coding: utf-8 -*-

from django.apps import AppConfig


class RegistrationConfig(AppConfig):
    """Registration application configuration."""

    name = 'djspace.registration'
    verbose_name = 'Registration Application'

    def ready(self):
        """Initiate the app."""
        import djspace.registration.signals
