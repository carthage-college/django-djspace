from django.contrib import admin
from django.conf.urls import patterns, url

urlpatterns = patterns('djspace.dashboard.views',
    url(
        r'^get-users/$',
        'get_users', name="get_users"
    ),
    url(
        r'^set-val/$',
        'set_val', name="set_val"
    ),
    url(
        r'^registration-type/$',
        'registration_type', name="registration_type"
    ),
    url(
        r'^profile/$',
        'profile_form', name="dashboard_profile"
    ),
    url(
        r'^$',
        'home', name="dashboard_home"
    ),
)
