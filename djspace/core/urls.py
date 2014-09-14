from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView, TemplateView

from django.contrib import admin

admin.autodiscover()

handler404 = 'djtools.views.errors.four_oh_four_error'
handler500 = 'djtools.views.errors.server_error'

urlpatterns = patterns('',
    url(
        r'^admin/', include(admin.site.urls)
    ),
    # registration
    url(
        r'^registration/', include("djspace.registration.urls")
    ),
    # redirect
    url(
        r'^$', RedirectView.as_view(url="/foobar/")
    ),
)
