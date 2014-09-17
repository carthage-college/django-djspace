from django.contrib import admin
from django.conf.urls import patterns, url
from django.views.generic import TemplateView

#django discovery
admin.autodiscover()

urlpatterns = patterns('djspace.registration.views',
    url(r'undergraduate', 'undergrad', name='undergrad_form'),
    url(r'graduate', 'graduate', name='graduate_form'),
    url(r'professional', 'professional', name='professional_form'),
    url(r'faculty', 'professor', name='faculty_form'),
    url(
        r'success',
        TemplateView.as_view(
            template_name='registration/success.html'
        ),
        name='registration_success'
    ),
    #url(
    #    r'^(?P<reg_type>[a-zA-Z0-9_-]+)/$',
    #    'form', name="registration_form"
    #),
)
