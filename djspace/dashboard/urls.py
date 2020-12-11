# -*- coding: utf-8 -*-

"""URLs for all views."""

from django.urls import path
from djspace.dashboard import views


urlpatterns = [
    path('get-users/', views.get_users, name='get_users'),
    path('set-val/', views.set_val, name='set_val'),
    path(
        'registration-type/',
        views.registration_type,
        name='registration_type',
    ),
    path('profile/', views.profile_form, name='dashboard_profile'),
    path('', views.home, name='dashboard_home'),
]
