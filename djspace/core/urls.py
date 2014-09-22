from django.conf.urls import patterns, include, url

from django.contrib import admin

admin.autodiscover()

handler404 = 'djtools.views.errors.four_oh_four_error'
handler500 = 'djtools.views.errors.server_error'

urlpatterns = patterns('',
    url(
        r'^accounts/', include('allauth.urls')
    ),
    url(
        r'^admin/', include(admin.site.urls)
    ),
    url(
        r'^dashboard/', include('djspace.dashboard.urls')
    ),
    # registration
    url(
        r'^registration/', include("djspace.registration.urls")
    ),
)
