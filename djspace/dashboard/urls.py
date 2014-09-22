from django.contrib import admin
from django.conf.urls import patterns, url
from django.views.generic import TemplateView

#django discovery
admin.autodiscover()

urlpatterns = patterns('djspace.dashboard.views',
    url(
        r'^$',
        'home', name="dashboard_home"
    ),
)
