from django.contrib import admin
from django.conf.urls import patterns, url
from django.views.generic import TemplateView

urlpatterns = patterns('djspace.registration.views',
    url(
        r'^success/$',
        TemplateView.as_view(
            template_name='registration/success.html'
        ),
        name='registration_success'
    ),
    url(
        r'^(?P<reg_type>[a-zA-Z0-9_-]+)/$',
        'form', name="registration_form"
    ),
)
