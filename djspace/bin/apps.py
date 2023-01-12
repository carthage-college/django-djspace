#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import django
import os
import sys
import argparse
import logging

# env
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djspace.settings.shell')

# required if using django models
django.setup()

from django.conf import settings
from django.contrib.auth.models import User
from djspace.core.utils import get_start_date

logger = logging.getLogger('debug_logfile')

# set up command-line options
desc = """
Accepts as input username
"""

# RawTextHelpFormatter method allows for new lines in help text
parser = argparse.ArgumentParser(
    description=desc, formatter_class=argparse.RawTextHelpFormatter,
)

parser.add_argument(
    '-u',
    '--username',
    required=True,
    help="Provide a username.",
    dest='username',
)
parser.add_argument(
    '--test',
    action='store_true',
    help="Dry run?",
    dest='test',
)


def main():
    """Main function description."""
    user = User.objects.get(username=username)
    start_date = get_start_date()
    apps = user.profile.applications
    for app in apps.all().order_by('-id'):
        if app.date_created >= start_date:
            print(app.id)


if __name__ == '__main__':
    args = parser.parse_args()
    username = args.username
    test = args.test

    if test:
        print(args)

    sys.exit(main())
