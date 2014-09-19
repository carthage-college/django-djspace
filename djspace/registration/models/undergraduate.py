# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import models, connection
from django.contrib.auth.models import User

from djspace.registration.models.base_models import *

UNDERGRADUATE_DEGREE = (
    ("Bachelor's degree","Bachelor's degree"),
    ("Associate's degree/certificate","Associate's degree/certificate")
)

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