from django.contrib import admin
from django.conf.urls import patterns, url

urlpatterns = patterns('djspace.dashboard.views',
    url(
        r'^$',
        'home', name="dashboard_home"
    ),
)
