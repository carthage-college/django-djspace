# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import models, connection
from django.contrib.auth.models import User  


class BaseLocationInformation(models.Model):
    
    name = models.CharField(
        "Name",
        max_length=25
    )
    street = models.CharField(
        "Street",
        max_length=35
    )
    city = models.CharField(
        "City",
        max_length=30
    )
    state = models.CharField(
        "State",
        max_length=20
    )
    zip_code = models.CharField(
        "ZIP code",
        max_length=11
    )
