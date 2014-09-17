# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import models, connection
from django.contrib.auth.models import User

from djspace.registration.models.base_models import *

class Faculty(BasePersonal, BaseEmployer):

    campus_email = models.EmailField(
        "Campus email address"
    )
    address_1 = models.CharField(
        "Address line 1",
        max_length=128
    )
    address_2 = models.CharField(
        "Address line 2",
        max_length=128
    )
    graduate_first = models.CharField(
        "First of your sibilings to graduate from college",
        max_length=6,
        choices=BINARY_CHOICES
    )
    subsidized_lunch = models.CharField(
        "Did you qualify for a subsidized school lunch",
        max_length=6,
        choices=BINARY_CHOICES
    )
    us_vet = models.CharField(
        "US Veteran of the Military",
        max_length=6,
        choices=BINARY_CHOICES
    )
