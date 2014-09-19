# -*- coding: utf-8 -*-
from django.db import models

from djspace.registration.models.base_models import *
from djspace.registration.validators import *

class Graduate(BasePersonal, BaseWSGC, BaseUndergrad):

    degree_program_other = models.CharField(
        "Other",
        max_length=128,
        blank=True
    )
    concentration_area = models.CharField(
        "Concentration area (eg. physics, astronomy, physiology, etc.)",
        max_length=128
    )
    graduate_gpa = models.FloatField(
        "Current cumulative GPA",
        max_length=4,
        validators=[credit_gpa_validator]
    )
    graduate_scale = models.IntegerField(
        "GPA Scale",
        max_length=4,
        validators=[credit_gpa_validator]
    )
    graduate_graduation_year = models.CharField(
        "Anticipated graduation year",
        max_length=4,
        validators=[four_digit_year_validator]
    )
