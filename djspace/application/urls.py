from django.contrib import admin
from django.conf.urls import patterns, url
from django.views.generic import TemplateView

urlpatterns = patterns('djspace.application.views',
    url(
        r'^success/$',
        TemplateView.as_view(
            template_name='myapp/success.html'
        ),
        name='myapp_success'
    ),
    url(
        r'^(?P<app_type>[a-zA-Z0-9_-]+)/$',
        'form', name="application_form"
    ),
)
