from django.contrib import admin
from django.conf.urls import url
from django.views.generic import TemplateView

from djspace.registration import views

urlpatterns = [
    url(
        r'^success/$',
        TemplateView.as_view(
            template_name='registration/success.html'
        ),
        name='registration_success'
    ),
    url(
        r'^(?P<uid>\d+)/print/$',
        views.registration_print, name='registration_print'
    ),
    url(
        r'^(?P<reg_type>[a-zA-Z0-9_-]+)/$',
        views.form, name='registration_form'
    )
]
