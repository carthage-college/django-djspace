# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import models, connection
from django.contrib.auth.models import User

from djspace.registration.models.base_models import *

class UndergraduateInformation(BasePersonalInformation, BaseWSGCInformation, BaseHighschoolInformation, BaseUndergradInformation):
    
    degree_seeking = models.CharField(
        "Degree seeking",
        max_length=20,
        choices=PROFESSION
    )
    ultimate_degree_seeking = models.CharField(
        "Ultimate degree seeking",
        max_length=20,
        choices=PROFESSION
    )
    sat_verbal = models.IntegerField(
        "SAT Verbal",
        max_length=4
    )
    sat_math = models.IntegerField(
        "SAT Math",
        max_length=4
    )
    sat_total = models.IntegerField(
        "SAT Total",
        max_length=4
    )
    act_english = models.IntegerField(
        "ACT English",
        max_length=2
    )
    act_math = models.IntegerField(
        "ACT Math",
        max_length=2
    )
    act_reading = models.IntegerField(
        "ACT Reading",
        max_length=2
    )
    act_science = models.IntegerField(
        "ACT Science",
        max_length=2
    )
    act_composite = models.IntegerField(
        "ACT Composite",
        max_length=2
    )
    gpa_major = models.FloatField(
        "Major GPA",
        max_length=4
    )    
    year_in_school = models.IntegerField(
        "Year in school as of next fall",
        max_length=4
    )    
    undergraduate_concentration = models.CharField(
        "Area of Undergraduate Concentration in a Space, Aerospace, or Space-Related Field",
        max_length=20
    )
