from django.contrib import admin
from django.views.generic import RedirectView
from django.core.urlresolvers import reverse_lazy
from django.conf.urls import include, url

from djspace.core import views
from djtools.views.dashboard import responsive_switch

from allauth.account.views import login

handler404 = 'djtools.views.errors.four_oh_four_error'
handler500 = 'djtools.views.errors.server_error'


urlpatterns = [
    # required files after funding granted
    url(
        r'^account/user-files-test/$',
        views.user_files_test, name='user_files_test'
    ),
    url(
        r'^account/user-files/$',
        views.user_files, name='user_files'
    ),
    # check files status
    url(
        r'^account/files-status/$',
        views.check_files_status, name='files_status'
    ),
    # upload optional photos
    url(
        r'^photo-upload/$',
        views.photo_upload, name='photo_upload'
    ),
    # account management
    url(
        r'^account/', include('allauth.urls')
    ),
    url(r'^account/login/$', login, name="auth_login"),
    # grants applications
    url(
        r'^application/', include('djspace.application.urls')
    ),
    # admin actions
    url(
        r'^(.+)/sendmail/$',
        views.sendmail, name='sendmail'
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
        r'^registration/', include('djspace.registration.urls')
    ),
    # delete an object
    url(
        r'^object-delete/$',
        views.object_delete, name='object_delete'
    ),
    # home
    url(
        r'^$',
        RedirectView.as_view(url=reverse_lazy('dashboard_home'))
    )
]
urlpatterns += url("admin/", include('loginas.urls')),
