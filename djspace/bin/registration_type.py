#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import django
import json
import logging
import os
import sys

# env
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djspace.settings.shell')

# required if using django models
django.setup()

from django.conf import settings
from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from django.http import Http404
from django.template import loader
from djspace.application.forms import *
from djtools.utils.convert import str_to_class
from pprint import pprint


logger = logging.getLogger('debug_logfile')

# set up command-line options
desc = """
Accepts as input a registration type.
"""

# RawTextHelpFormatter method allows for new lines in help text
parser = argparse.ArgumentParser(
    description=desc, formatter_class=argparse.RawTextHelpFormatter,
)

parser.add_argument(
    '-r',
    '--registration',
    required=True,
    help="Provide a username.",
    dest='reg_type',
)
parser.add_argument(
    '--test',
    action='store_true',
    help="Dry run?",
    dest='test',
)


def main():
    """AJAX post for retrieving registration forms based on type."""
    jason = {}
    user = User.objects.get(pk=1)
    try:
        mod = django.apps.apps.get_model(
            app_label='registration', model_name=reg_type,
        )
        reg = mod.objects.get(user=user)
    except Exception:
        reg = None
    try:
        reg_form = str_to_class(
            'djspace.registration.forms',
            '{0}Form'.format(reg_type),
        )(instance=reg, prefix='reg', use_required_attribute=False)
    except Exception:
        raise Http404
    reggie = None
    print('mod = {0}'.format(mod))
    print('reg = {0}'.format(reg))
    if reg:
        reggie = model_to_dict(reg)
        print('reggie = ')
        pprint(reggie)
        # remove some fields because json barfs on them and we don't need it
        if 'cv' in reggie.keys():
            reggie['cv'] = ''
        if 'programs' in reggie.keys():
            reggie['programs'] = ''
    template = loader.get_template('dashboard/registration_form.inc.html')
    context = {'reg_form': reg_form, 'reg_type': reg_type}
    jason = {
        'form': template.render(context, None),
        'reg': reggie,
        'reg_type': reg_type,
    }
    pprint(json.dumps(jason))


if __name__ == '__main__':
    args = parser.parse_args()
    reg_type = args.reg_type
    test = args.test

    if test:
        print(args)

    sys.exit(main())
