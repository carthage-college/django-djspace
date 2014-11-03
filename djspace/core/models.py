# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

from djtools.fields import BINARY_CHOICES, YES_NO_DECLINE, STATE_CHOICES
from djtools.fields import GENDER_CHOICES, SALUTATION_TITLES

from djspace.registration.models import *

from taggit.managers import TaggableManager
from gm2m import GM2MField

from datetime import date

REG_TYPE = (
    ('','----select----'),
    ('Undergraduate','Undergraduate'),
    ('Graduate','Graduate'),
    ('Faculty','Faculty'),
    ('Professional','Professional')
)

BIRTH_YEAR_CHOICES = [x for x in reversed(xrange(1926,date.today().year -16))]

class GenericChoice(models.Model):
    """
    For making choices for choice fields for forms
    """
    name = models.CharField(
        unique=True, max_length=255
    )
    value = models.CharField(
        max_length=255
    )
    ranking = models.IntegerField(
        null=True, blank=True, default=0,
        max_length=3,
        verbose_name="Ranking",
        help_text=
        """
        A number from 0 to 999 to determine this object's position in a list.
        """
    )
    active = models.BooleanField(
        help_text=
        """
        Do you want the field to be visable on your form?
        """,
        verbose_name="Is active?",
        default=True
    )
    tags = TaggableManager()

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['ranking']

class UserProfile(models.Model):

    # meta
    user = models.OneToOneField(
        User, related_name="profile"
    )
    updated_by = models.ForeignKey(
        User, verbose_name="Updated by",
        related_name="user_profile_updated_by",
        editable=False
    )
    date_created = models.DateTimeField(
        "Date Created", auto_now_add=True
    )
    date_updated = models.DateTimeField(
        "Date Updated", auto_now=True
    )
    # core
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
    race = models.ManyToManyField(
        GenericChoice,
        related_name="user_profile_race",
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
    applications = GM2MField()


    def __unicode__(self):
        return "%s %s's profile" % (self.user.first_name, self.user.last_name)

    def get_registration(self):
        try:
            return eval(self.registration_type).objects.get(user=self.user)
        except:
            return None
