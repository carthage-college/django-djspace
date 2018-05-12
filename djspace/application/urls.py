from django.contrib import admin
from django.conf.urls import url
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

from djspace.application import views

urlpatterns = [
    url(
        r'^$',
        login_required(TemplateView.as_view(
            template_name='application/home.html'
        )),
        name='application_home'
    ),
    url(
        r'^success/$',
        login_required(TemplateView.as_view(
            template_name='application/success.html'
        )),
        name='application_success'
    ),
    url(
        r'^get-program-submissions/$',
        views.get_program_submissions, name='get_program_submissions'
    ),
    url(
        r'^(?P<application_type>[a-zA-Z0-9_-]+)/(?P<aid>\d+)/print/$',
        views.application_print, name='application_print'
    ),
    url(
        r'^(?P<application_type>[a-zA-Z0-9_-]+)/(?P<aid>\d+)/update/$',
        views.application_form, name='application_update'
    ),
    url(
        r'^(?P<application_type>[a-zA-Z0-9_-]+)/export/$',
        views.application_export, name='application_export'
    ),
    url(
        r'^(?P<application_type>[a-zA-Z0-9_-]+)/$',
        views.application_form, name='application_create'
    ),
]
