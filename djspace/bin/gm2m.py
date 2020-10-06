# -*- coding: utf-8 -*-
import os
import sys

# env
sys.path.append('/usr/lib/python2.7/dist-packages/')
sys.path.append('/usr/lib/python2.7/')
sys.path.append('/usr/local/lib/python2.7/dist-packages/')
sys.path.append('/data2/django_1.11/')
sys.path.append('/data2/django_projects/')
sys.path.append('/data2/django_third/')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djspace.settings')

import django
django.setup()

from django.contrib.auth.models import User

#users = User.objects.all().order_by('last_name')
user = User.objects.get(pk=)

apps = user.profile.applications.all()

print apps
'''
if apps:
    for a in apps:
        #print a
        print a.__dict__
        #print a._state.__dict__
        #print a.id
        # don't work
        #print a.all()
        #print a.get_related_models()
'''
