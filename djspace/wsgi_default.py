# -*- coding: utf-8 -*-

"""WSGI configuration."""

import os
import sys

# python
sys.path.append('/data2/python_venv/2.7/djspace/lib/python2.7/')
sys.path.append('/data2/python_venv/2.7/djspace/lib/python2.7/site-packages/')
sys.path.append('/data2/python_venv/2.7/djspace/lib/django_projects/')
sys.path.append('/data2/python_venv/2.7/djspace/lib/django-djspace/')
# django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djspace.settings.production')
os.environ.setdefault('PYTHON_EGG_CACHE', '')
os.environ.setdefault('TZ', 'America/Chicago')
# wsgi
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
