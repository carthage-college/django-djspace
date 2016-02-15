import os
import time
import traceback
import signal
import sys

# python
sys.path.append('/usr/lib/python2.7/')
sys.path.append('/usr/lib/python2.7/dist-packages/')
sys.path.append('/usr/local/lib/python2.7/dist-packages/')
sys.path.append('/data2/django_current/')
sys.path.append('/data2/django_projects/')
sys.path.append('/data2/django_third/')
# django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djspace.settings")
os.environ.setdefault("PYTHON_EGG_CACHE", "/var/cache/python/.python-eggs")
os.environ.setdefault("TZ", "America/Chicago")

# wsgi
from django.core.wsgi import get_wsgi_application

try:
    application = get_wsgi_application()
    #print 'WSGI without exception'
except Exception:
    #print 'handling WSGI exception'
    # Error loading applications
    if 'mod_wsgi' in sys.modules:
        traceback.print_exc()
        os.kill(os.getpid(), signal.SIGINT)
        time.sleep(2.5)


