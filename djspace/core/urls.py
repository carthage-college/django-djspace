# -*- coding: utf-8 -*-

"""URLs for all views."""

from allauth.account.views import login
from django.contrib import admin
from django.urls import include
from django.urls import path
from django.urls import re_path
from django.urls import reverse_lazy
from django.views.generic import RedirectView
from djspace.core import views


handler404 = 'djtools.views.errors.four_oh_four_error'
handler500 = 'djtools.views.errors.server_error'


urlpatterns = [
    # django admin
    path('admin/', include('loginas.urls')),
    path('admin/', admin.site.urls),
    # required files after funding granted
    path(
        'account/user-files-test/',
        views.user_files_test,
        name='user_files_test',
    ),
    # download user files with a name that matches the program
    path(
        'account/user-files/<str:field>/<str:ct>/<int:oid>/<str:uid>/download/',
        views.download_file,
        name='download_file',
    ),
    # Update user files via ajax post
    path('account/user-files/', views.user_files, name='user_files'),
    # check files status
    path('account/files-status/', views.check_files_status, name='files_status'),
    # upload optional photos
    path('photo-upload/', views.photo_upload, name='photo_upload'),
    # account management
    path('account/', include('allauth.urls')),
    path('account/login/', login, name='auth_login'),
    # grants applications
    path('application/', include('djspace.application.urls')),
    # admin actions
    path('sendmail/', views.sendmail, name='sendmail'),
    # registered users dashboard
    path('dashboard/', include('djspace.dashboard.urls')),
    # registration
    path('registration/', include('djspace.registration.urls')),
    # delete an object
    path('object-delete/', views.object_delete, name='object_delete'),
    # home
    path('', RedirectView.as_view(url=reverse_lazy('dashboard_home'))),
]
