from django.contrib import admin
from django.conf.urls import patterns, url
from django.views.generic import TemplateView

#django discovery
admin.autodiscover()

urlpatterns = patterns('djspace.registration.views',
    url(r'^/test/undergrad$', 'undergrad', name='undergrad'),
    url(
        r'^myview/(?P<pid>\d+)/$',
        'myview', name="myapp_display"
    ),
    url(
        r'^search/$',
        'search', name="myapp_search"
    ),
    url(
        r'^myview/success/$',
        TemplateView.as_view(
            template_name='myapp/success.html'
        ),
        name='myapp_success'
    ),
)
