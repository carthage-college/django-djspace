# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import models, connection
from django.contrib.auth.models import User

from djspace.registration.models.base_models import *

class Graduate(BasePersonal, BaseWSGC, BaseUndergrad, BaseCollege):

    degree_program = models.CharField(
        "What degree program are you enrolled in?",
        max_length=128,
        choices=GRADUATE_DEGREE
    )
    degree_program_other = models.CharField(
        "Other",
        max_length=128,
        blank=True
    )
    undergraduate_honors = models.CharField(
        "Undergraduate honors",
        max_length=20
    )
    gre_verbal = models.IntegerField(
        "GRE Verbal",
        max_length=3
    )
    gre_quantitative = models.IntegerField(
        "GRE Quantitative",
        max_length=3
    )
    gre_analytic = models.IntegerField(
        "GRE Analytic",
        max_length=3
    )
    test = models.CharField(
        "Other test",
        max_length=20
    )
    test_score = models.CharField(
        "Score",
        max_length=10
    )
    degree_seeking = models.CharField(
        "Degree seeking",
        max_length=20,
        choices=GRADUATE_DEGREE
    )
    ultimate_degree_seeking = models.CharField(
        "Ultimate degree seeking",
        max_length=20,
        choices=GRADUATE_DEGREE
    )
    # Going to need select options later
    graduate_major = models.CharField(
        "Major",
        max_length=20
    )
    graduate_emphasis = models.CharField(
        "Emphasis",
        max_length=20
    )
    graduate_gpa = models.FloatField(
        "Current cumulative GPA",
        max_length=4
    )
    graduate_gpa_major = models.FloatField(
        "Major GPA",
        max_length=4
    )
    graduate_scale = models.IntegerField(
        "Scale",
        max_length=1
    )
    graduate_CREDITS = models.FloatField(
        "Credits",
        max_length=5
    )
    graduate_year_in_school = models.IntegerField(
        "Year in school as of next fall",
        max_length=4
    )
    graduate_graduation = models.DateField(
        "Expected date of graduation",
        auto_now=False
    )
