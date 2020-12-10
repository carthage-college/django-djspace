# -*- coding: utf-8 -*-

"""URLs for all views."""

from django.contrib.auth.decorators import login_required
from django.urls import path
from django.views.generic import TemplateView

from djspace.application import views


urlpatterns = [
    path(
        '',
        login_required(TemplateView.as_view(
            template_name='application/home.html',
        )),
        name='application_home',
    ),
    path(
        'success/',
        login_required(TemplateView.as_view(
            template_name='application/success.html',
        )),
        name='application_success',
    ),
    path(
        'get-program-submissions/',
        views.get_program_submissions,
        name='get_program_submissions',
    ),
    path(
        '<str:application_type>/<int:aid>/print/',
        views.application_print,
        name='application_print',
    ),
    path(
        '<str:application_type>/<int:aid>/update/',
        views.application_form,
        name='application_update',
    ),
    path(
        '<str:application_type>/export/',
        views.application_export,
        name='application_export',
    ),
    path(
        '<str:application_type>/',
        views.application_form,
        name='application_create',
    ),
]
