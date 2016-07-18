from django.contrib import admin
from django.views.generic import RedirectView
from django.core.urlresolvers import reverse_lazy
from django.conf.urls import patterns, include, url

from djtools.views.dashboard import responsive_switch

handler404 = 'djtools.views.errors.four_oh_four_error'
handler500 = 'djtools.views.errors.server_error'

urlpatterns = patterns('',
    # account management
    url(
        r'^account/', include('allauth.urls')
    ),
    # grants applications
    url(
        r'^application/', include('djspace.application.urls')
    ),
    # django admin
    url(
        r'^admin/', include(admin.site.urls)
    ),
    # registered users dashboard
    url(
        r'^dashboard/', include('djspace.dashboard.urls')
    ),
    # registration
    url(
        r'^registration/', include("djspace.registration.urls")
    ),
    # home
    url(
        r'^$',
        RedirectView.as_view(url=reverse_lazy("dashboard_home"))
    )
)
