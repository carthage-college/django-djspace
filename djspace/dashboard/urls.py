from django.contrib import admin
from django.conf.urls import url

from djspace.dashboard import views

urlpatterns = [
    url(
        r'^get-users/$',
        views.get_users, name='get_users'
    ),
    url(
        r'^set-val/$',
        views.set_val, name='set_val'
    ),
    url(
        r'^registration-type/$',
        views.registration_type, name='registration_type'
    ),
    url(
        r'^profile/$',
        views.profile_form, name='dashboard_profile'
    ),
    url(
        r'^$',
        views.home, name='dashboard_home'
    )
]
