#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import django
import os
import sys


django.setup()

# env
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djspace.settings.shell')

from django.contrib.auth.models import User

user = User.objects.get(pk=1217743)
print(user)

apps = user.profile.applications.all()

print(apps)
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
