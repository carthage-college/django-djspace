# -*- coding: utf-8 -*-

"""Django settings for project."""

import os


DEBUG = False
ADMINS = ()
MANAGERS = ADMINS
SECRET_KEY = ''
ALLOWED_HOSTS = ['localhost', '127.0.0.1']
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/Chicago'
SITE_ID = 1
USE_I18N = True
USE_L10N = False
USE_TZ = False
DEFAULT_CHARSET = 'utf-8'
FILE_CHARSET = 'utf-8'
SERVER_URL = ''
LIVEWHALE_API_URL = 'https://{0}'.format(SERVER_URL)
WSGI_APPLICATION = 'djspace.wsgi.application'
ROOT_URLCONF = 'djspace.core.urls'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT_DIR = BASE_DIR
PROJECT_APP = os.path.basename(BASE_DIR)
ROOT_URL = '/apps/'
ADMIN_MEDIA_PREFIX = '/static/admin/'
MEDIA_ROOT = '{0}/assets/'.format(ROOT_DIR)
STATIC_ROOT = '{0}/static/'.format(ROOT_DIR)
STATIC_URL = '/static/{0}/'.format(PROJECT_APP)
MEDIA_URL = '/media/{0}/'.format(PROJECT_APP)
UPLOADS_DIR = '{0}files/'.format(MEDIA_ROOT)
UPLOADS_URL = '{0}files/'.format(MEDIA_URL)
FILE_UPLOAD_PERMISSIONS = 0o644
STATICFILES_DIRS = ()
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'
DATABASES = {
    'default': {
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'django_djspace',
        'USER': '',
        'PASSWORD': '',
    },
}
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.messages',
    # needed for allauth
    'django.contrib.sites',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    # registration and authentication
    'allauth',
    'allauth.account',
    # gmail api for send mail
    'gmailapi_backend',
    # generice many to many
    'gm2m',
    # sign in as user
    'loginas',
    # tagging
    'taggit',
    # core
    'djspace.application',
    'djspace.registration',
    'djspace.core',
    'djtools',
)
MIDDLEWARE = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
)

# template stuff
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
            '/data2/django_templates/djeuropa/',
            '/data2/django_templates/djcher/',
        ],
        'OPTIONS': {
            'debug': DEBUG,
            'context_processors': [
                'djtools.context_processors.sitevars',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.media',
                'django.template.context_processors.request',
                'django.template.context_processors.static',
                'django.contrib.messages.context_processors.messages',
            ],
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
        },
    },
]
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.PyMemcacheCache',
        'LOCATION': '127.0.0.1:11211',
        'TIMEOUT': 604800,
        'KEY_PREFIX': '{0}_'.format(PROJECT_APP),
    }
}
# auth backends
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    # allauth specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)
LOGIN_URL = '{0}accounts/login/'.format(ROOT_URL)
LOGOUT_URL = '{0}accounts/logout/'.format(ROOT_URL)
LOGIN_REDIRECT_URL = '{0}dashboard/'.format(ROOT_URL)
USE_X_FORWARDED_HOST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_COOKIE_DOMAIN = ''
SESSION_COOKIE_NAME = ''
SESSION_COOKIE_AGE = 86400
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
# gmail API settings
EMAIL_FROM = ''
GMAIL_USER = ''
EMAIL_BACKEND = 'gmailapi_backend.service.GmailApiBackend'
GMAIL_SCOPES = ['https://www.googleapis.com/auth/gmail.send']
GMAIL_SERVICE_ACCOUNT_JSON = ''
GOOGLE_SERVICE_ACCOUNT = ''
# system email addresses
DEFAULT_FROM_EMAIL = ''
SERVER_EMAIL = ''
SERVER_MAIL = ''
# logging
LOG_FILEPATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'logs/',
)
LOG_FILENAME = '{0}{1}'.format(LOG_FILEPATH, 'debug.log')
DEBUG_LOG_FILENAME = '{0}{1}'.format(LOG_FILEPATH, 'debug.log')
INFO_LOG_FILENAME = '{0}{1}'.format(LOG_FILEPATH, 'info.log')
ERROR_LOG_FILENAME = '{0}{1}'.format(LOG_FILEPATH, 'error.log')
CUSTOM_LOG_FILENAME = '{0}{1}'.format(LOG_FILEPATH, 'custom.log')
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s',
            'datefmt': '%Y/%b/%d %H:%M:%S',
        },
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s',
            'datefmt': '%Y/%b/%d %H:%M:%S',
        },
        'simple': {
            'format': '%(levelname)s %(message)s',
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'logfile': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': LOG_FILENAME,
            'formatter': 'standard',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'include_html': True,
            'class': 'django.utils.log.AdminEmailHandler',
        },
    },
    'loggers': {
        'custom_logfile': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': CUSTOM_LOG_FILENAME,
            'formatter': 'custom',
        },
        'info_logfile': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'backupCount': 10,
            'maxBytes': 50000,
            'filename': INFO_LOG_FILENAME,
            'formatter': 'simple',
        },
        'debug_logfile': {
            'level': 'DEBUG',
            'handlers': ['logfile'],
            'class': 'logging.FileHandler',
            'filename': DEBUG_LOG_FILENAME,
            'formatter': 'verbose',
        },
        'error_logfile': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': ERROR_LOG_FILENAME,
            'formatter': 'verbose',
        },
        'django': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'WARN',
        },
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}
#
# app config
#
ENCRYPTION_KEY = b''
WSGC_EMAIL = ''
WSGC_APPLICATIONS = ''
WSGC_ROCKET_EMAIL = ''
ROCKET_LAUNCH_COMPETITION_TEAM_LIMIT = 100
FILE_UPLOADED_EMAILS = {
    'all': [],
    'rocketlaunchteam': [],
    'firstnationsrocketcompetition': [],
    'collegiaterocketcompetition': [],
}
# the month after which the new grant cycle begins
GRANT_CYCLE_START_MES = 8
# allauth configuration
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_EMAIL_SUBJECT_PREFIX = '[WSGC] '
ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'https'
ACCOUNT_LOGIN_REDIRECT_URL = '{0}dashboard/'.format(ROOT_URL)
ACCOUNT_LOGOUT_REDIRECT_URL = ROOT_URL
ACCOUNT_SIGNUP_FORM_CLASS = 'djspace.core.forms.SignupForm'
ACCOUNT_SIGNUP_PASSWORD_VERIFICATION = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USER_MODEL_USERNAME_FIELD = 'username'
ACCOUNT_USER_MODEL_EMAIL_FIELD = 'email'
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_PASSWORD_MIN_LENGTH = 8
ACCOUNT_SESSION_REMEMBER = None
ACCOUNT_SESSION_COOKIE_AGE = 86400

##################
# LOCAL SETTINGS #
##################

# Allow any settings to be defined in local.py which should be
# ignored in your version control system allowing for settings to be
# defined per machine.

# Instead of doing "from .local import *", we use exec so that
# local has full access to everything defined in this module.
# Also force into sys.modules so it's visible to Django's autoreload.

phile = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'local.py')
if os.path.exists(phile):
    import imp
    import sys
    module_name = '{0}.settings.local'.format(PROJECT_APP)
    module = imp.new_module(module_name)
    module.__file__ = phile
    sys.modules[module_name] = module
    exec(open(phile, 'rb').read())
