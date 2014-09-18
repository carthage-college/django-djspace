# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import models, connection
from django.contrib.auth.models import User

from djspace.registration.models.base_models import *

class Undergraduate(BasePersonal, BaseWSGC, BaseUndergrad):

    highschool_name = models.CharField(
        "High school name",
        max_length=128
    )
    highschool_street = models.CharField(
        "High school street",
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
    highschool_postal_code = models.CharField(
        "High school zip code",
        max_length=9
    )

    pass
    #undergraduate_concentration = models.CharField(
    #    "Area of Undergraduate Concentration in a Space, Aerospace, or Space-Related Field",
    #    max_length=20
    #)
