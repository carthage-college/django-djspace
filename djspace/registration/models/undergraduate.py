# -*- coding: utf-8 -*-
from django.db import models

from djspace.registration.models.base_models import *

class Undergraduate(BasePersonal, BaseWSGC, BaseUndergrad):

    highschool_name = models.CharField(
        "High school name",
        max_length=128
    )
    highschool_city = models.CharField(
        "High school city",
        max_length=128
    )
    highschool_state = models.CharField(
        "High school state",
        max_length=2,
        choices=STATE_CHOICES
    )
