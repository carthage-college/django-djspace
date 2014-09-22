# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

from djspace.registration.choices import RACES, REG_TYPE

from djtools.fields import BINARY_CHOICES, YES_NO_DECLINE, STATE_CHOICES
from djtools.fields import GENDER_CHOICES, SALUTATION_TITLES

class UserProfile(models.Model):
    user = models.OneToOneField(
        User, related_name="profile"
    )
    salutation = models.CharField(
        max_length=16,
        choices=SALUTATION_TITLES,
        null=True, blank=True
    )
    second_name = models.CharField(
        max_length=30,
        null=True, blank=True
    )
    address1 = models.CharField(
        "Address",
        max_length=128
    )
    address2 = models.CharField(
        "",
        max_length=128,
        null=True, blank=True
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
    phone = models.CharField(
        verbose_name='Phone number',
        max_length=12,
        help_text="Format: XXX-XXX-XXXX"
    )
    date_of_birth = models.DateField(
        "Date of birth",
        help_text="Format: mm/dd/yyyy"
    )
    gender = models.CharField(
        max_length=16,
        choices = GENDER_CHOICES
    )
    race = models.CharField(
        max_length=128,
        help_text = 'Check all that apply'
    )
    tribe = models.CharField(
        "Tribe",
        max_length=128,
        null=True, blank=True
    )
    disability = models.CharField(
        "Disability status",
        max_length=16,
        choices=YES_NO_DECLINE
    )
    us_citizen = models.CharField(
        "United States Citizen",
        max_length=4,
        choices=BINARY_CHOICES
    )
    registration_type = models.CharField(
        max_length=32,
        choices=REG_TYPE
    )

    def __unicode__(self):
        return "%s %s's profile" % (self.user.first_name, self.user.last_name)

