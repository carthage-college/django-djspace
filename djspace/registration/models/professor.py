# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import models, connection
from django.contrib.auth.models import User

from djspace.registration.models.base_models import *

class ProfessorInformation(BasePersonal, BaseEmployer):
    
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
