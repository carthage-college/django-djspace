from django.contrib import admin
from django.conf.urls import patterns, url
from django.views.generic import TemplateView

#django discovery
admin.autodiscover()

urlpatterns = patterns('djspace.application.views',
    url(r'^test/0$', 'undergrad', name='undergrad form'),
    url(r'^test/1$', 'graduate', name='graduate form'),
    url(r'^test/2$', 'professional', name='professional form'),
    url(r'^test/3$', 'professor', name='professor form'),
    #url(r'^test/4$', 'k12educator', name='k12 educator form'),
    url(
        r'^myview/success/$',
        TemplateView.as_view(
            template_name='myapp/success.html'
        ),
        name='myapp_success'
    ),
    url(
        r'^(?P<reg_type>[a-zA-Z0-9_-]+)/$',
        'form', name="application_form"
    ),
)
