# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import models, connection
from django.contrib.auth.models import User  


class BasePersonalInformation(models.Model):
    
    GENDER = (
     ('male','Male'),('female','Female')   
    )
    
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
    email = models.EmailField(
        "Email address" 
    )
    birth = models.DateField(
        "Birthdate",
        auto_now=False
    )
    phone = models.CharField(
        "Phone number",
        max_length=16
    )
    gender = models.CharField(
        "Gender",
        max_length=8,
        choices=GENDER
    )
    

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
