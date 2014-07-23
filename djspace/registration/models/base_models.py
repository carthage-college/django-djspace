# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import models, connection
from django.contrib.auth.models import User

from djtools.fields import BINARY_CHOICES, SALUTATION_TITLES, STATE_CHOICES
from djtools.fields import GENDER_CHOICES


class BaseInformationModel(models.Model):

  first = models.CharField(
    "First name",
    max_length=20
  )
  middle = models.CharField(
    "Middle name",
    max_length=20
  )
  last = models.CharField(
    "Last name",
    max_length=20
  )
  citizen = models.BooleanField(
    "US Citizen"
  )
  rocket_comp = models.BooleanField(
    "Tribal or AISES Rocket Competition"
  )
  maiden = models.CharField(
    "Maiden name",
    max_length=20
  )
  additional = models.CharField(
    "Additional name",
    max_length=20
  )
  title_department = models.CharField(
    "Title or Department",
    max_length=20
  )
  webpage = models.CharField(
    "Web page",
    max_length=20
  )
  street = models.CharField(
    "Street",
    max_length=20
  )
  city = models.CharField(
    "City",
    max_length=20
  )
  state = models.CharField(
    "State",
    max_length=2,
    choices=STATE_CHOICES
  )
  ZIP = models.CharField(
    "Zip code",
    max_length=9
  )
  phone = models.CharField(
    "Phone number",
    max_length=16
  )
  primary = models.CharField(
    "Primary interest",
    max_length=35,
    choices=INTEREST
  )
  primary_other = models.CharField(
    "Other",
    max_length=35
  )
  secondary = models.CharField(
    "Secondary interest",
    max_length=35,
    choices=INTEREST
  )
  secondary_other = models.CharField(
    "Other",
    max_length=35
  )
  birthdate = models.DateField(
    "Birthdate",
    auto_now=False
  )
  gender = models.CharField(
    "Gender",
    max_length=8,
    choices=GENDER_CHOICES
  )
  disability = models.BooleanField(
    "Disability"
  )
  race = models.CharField(
    "Race",
    max_length=25,
    choices=RACE
  )
  tribe = models.CharField(
    "Tribe",
    max_length=20
  )
  
  
  
class BaseEmployerInformation(models.Model):

  employer = models.CharField(
        "Employer",
        max_length=20,
        choices=EMPLOYER
    )
    employer_name = models.CharField(
        "Employer name",
        max_length=20,
        choices=EMPLOYER
    )
    employer_street = models.CharField(
        "Employer street",
        max_length=20
    )
    employer_city = models.CharField(
        "Employer city",
        max_length=20
    )
    employer_state = models.CharField(
        "Employer state",
        max_length=2,
        choices=STATE_CHOICES
    )
    employer_zip = models.CharField(
        "Employer zip code",
        max_length=9
    )
