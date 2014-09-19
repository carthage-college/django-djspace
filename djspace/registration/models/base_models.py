# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import models, connection
from django.contrib.auth.models import User

from djspace.registration.validators import *
from djspace.registration.choices import *

from djtools.fields import BINARY_CHOICES, SALUTATION_TITLES, STATE_CHOICES
from djtools.fields import GENDER_CHOICES

class BasePersonal(models.Model):

    salutation = models.CharField(
        "Salutation",
        max_length=16,
        null=True, blank=True
    )
    first_name = models.CharField(
        "First name",
        max_length=128
    )
    middle_initial = models.CharField(
        "Middle initial",
        max_length=1
    )
    last_name = models.CharField(
        "Last name",
        max_length=128
    )
    address_1 = models.CharField(
        "Address line 1",
        max_length=128
    )
    address_2 = models.CharField(
        "Address line 2",
        max_length=128,
        blank=True
    )
    city = models.CharField(
        "City",
        max_length=128
    )
    state = models.CharField(
        "State",
        max_length=2,
        choices=STATE_CHOICES
    )
    postal_code = models.CharField(
        "Zip code",
        max_length=9
    )
    email = models.EmailField(
        "Email"
    )
    disability = models.CharField(
        "Disability status",
        max_length=16,
        choices=YES_NO_DECLINE
    )
    tribe = models.CharField(
        "Tribe",
        max_length=128,
        blank=True
    )

    class Meta:
        abstract = True


class BaseWSGC(models.Model):

    wsgc_school = models.CharField(
        "WSGC College or University applied to",
        choices=WSGC_SCHOOL,
        max_length=128
    )

    class Meta:
        abstract = True


class BaseUndergrad(models.Model):

    # NEEDS TO BE A DROP DOWN
    major = models.CharField(
        "Primary major",
        max_length=20
    )
    major_other = models.CharField(
        "Other",
        max_length=128,
        blank=True
    )
    # NEEDS TO BE A DROP DOWN
    secondary_major_minor = models.CharField(
        "Secondary major or minor",
        max_length=128
    )
    secondary_major_minor_other = models.CharField(
        "Other",
        max_length=128,
        blank=True
    )
    student_id = models.CharField(
        "Student ID",
        max_length=7
    )
    current_cumulative_gpa = models.CharField(
        "Current cumulative GPA",
        max_length=4,
        validators=[credit_gpa_validator]
    )
    gpa_in_major = models.CharField(
        "GPA in major",
        max_length=4,
        validators=[credit_gpa_validator]
    )
    gpa_scale = models.CharField(
        "GPA scale",
        max_length=4,
        validators=[credit_gpa_validator]
    )
    cumulative_college_credits = models.CharField(
        "Cumulative college credits",
        max_length=6,
        validators=[credit_gpa_validator]
    )
    month_year_of_graduation = models.CharField(
        "Expected month and year of graduation",
        max_length=7,
        validators=[month_year_validator]
    )

    class Meta:
        abstract = True
