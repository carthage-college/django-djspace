# -*- coding: utf-8 -*-

"""URLs for all views."""

from django.urls import path
from django.views.generic import TemplateView
from djspace.registration.views import form
from djspace.registration.views import registration_print


urlpatterns = [
    path(
        'success/',
        TemplateView.as_view(template_name='registration/success.html'),
        name='registration_success',
    ),
    path('<int:pid>/print/', registration_print, name='registration_print'),
    path('<str:reg_type>/', form, name='registration_form'),
]
