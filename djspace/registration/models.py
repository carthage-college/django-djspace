# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import models, connection
from django.contrib.auth.models import User        

CITIZENSHIP = (
    ('us','Yes'),
    ('non-us','No'),
)

PROFESSION = (
    ('undergrad','Undergraduate'),
    ('graduate','Graduate'),
    ('professional','Professional'),
    ('professor','Professor'),
    ('k12educator','K12 Educator'),
)

SALUTATION = (
    ('mr','Mr'),
    ('ms','Ms'),
    ('mrs','Mrs'),
    ('dr','Dr'),
)

class PersonalInformation(models.Model):
    """
    Personal information when registering
    """
    
    rocket_contest = models.BooleanField(
        "Tribal or AISES Competition"
    )
    citizenship = models.CharField(
        "US Citizenship",
        max_length=7,
        choices=CITIZENSHIP
    )
    profession = models.CharField(
        "Profession",
        max_length=11,
        choices=PROFESSION
    )
    salutation = models.CharField(
        "Salutation",
        max_length=3,
        choices=SALUTATION
    )
    first = models.CharField(
        "First Name",
        max_length=20
    )
    middle = models.CharField(
        "Middle Name",
        max_length=15
    )
    last = models.CharField(
        "Last Name",
        max_length=20
    )
    maiden_name = models.CharField(
        "Maiden Name",
        max_length=20
    )
    #Do we need additional name? -zw
    additional_name = models.CharField(
        "Additional name",
        max_length=20
    )
    title_department = models.CharField(
        "Title or Department",
        max_length=40
    )
    #Consider renaming "web page" -zw
    web_page = models.CharField(
        "Web page",
        max_length=50
    )
