from django.contrib import admin
from django.conf.urls import patterns, url
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

urlpatterns = patterns('djspace.application.views',
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
        r'^(?P<application_type>[a-zA-Z0-9_-]+)/(?P<aid>\d+)/print/$',
        'application_print', name="application_print"
    ),
    url(
        r'^(?P<application_type>[a-zA-Z0-9_-]+)/(?P<aid>\d+)/update/$',
        'application_form', name="application_update"
    ),
    url(
        r'^(?P<application_type>[a-zA-Z0-9_-]+)/export/$',
        'application_export', name="application_export"
    ),
    url(
        r'^(?P<application_type>[a-zA-Z0-9_-]+)/$',
        'application_form', name="application_create"
    ),
)
