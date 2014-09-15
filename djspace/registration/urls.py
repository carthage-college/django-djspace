from django.contrib import admin
from django.conf.urls import patterns, url
from django.views.generic import TemplateView

#django discovery
admin.autodiscover()

urlpatterns = patterns('djspace.registration.views',
    url(r'^undergraduate$', 'undergrad', name='undergrad form'),
    url(r'^graduate$', 'graduate', name='graduate form'),
    url(r'^test/2$', 'professional', name='professional form'),
    url(r'^faculty$', 'faculty', name='faculty form'),
    url(r'^test/4$', 'k12educator', name='k12 educator form'),
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
