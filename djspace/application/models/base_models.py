# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import models, connection
from django.contrib.auth.models import User

from djtools.fields import BINARY_CHOICES, SALUTATION_TITLES, STATE_CHOICES
from djtools.fields import GENDER_CHOICES

GRAVITY_TRAVEL = (
    ('gravity','Reduced Gravity'),
    ('travel','Student Travel')
)

TITLE = (
    ('advisor','Faculty Advisor'),
    ('leader','Team Lead'),
    ('member','Member')
)

TIME_FRAME = (
    ('summer','Summer 6/1 - 8/15'),
    ('summerfall','Summer and Fall 6/1 - 12/10'),
    ('fall','Fall 8/15 - 12/10'),
    ('spring','Spring 12/10 - 5/1'),
    ('summerfallspring','Summer, Fall and Spring 6/1 - 5/1'),
    ('fallspring','Fall and Spring 8/15 - 5/1')
)

class BaseFacultyAdvisor(models.Model):
    
    title = models.CharField(
        "Title",
        max_length=20,
        choices=TITLE
    )
    team_name = models.CharField(
        "Team name",
        max_length=20
    )
    title = models.CharField(
        "Title of project",
        max_length=20
    )
    wsgc_funds = models.IntegerField(
        "WSGC funds requested",
        max_length=10
    )
    synopsis = models.CharField(
        "Project synopsis",
        max_length=100
    )
    FILE = models.FileField(
        "File upload",
        upload_to=None
    )
    select = models.CharField(
        "Select team",
        max_length=30
        #NEEDS A SELECT
    )
    

class StudentTravel(models.Model):
    
    purpose = models.CharField(
        "Purpose of travel",
        max_length=50
    )
    location = models.CharField(
        "Location of travel",
        max_length=20
    )
    time_frame = models.CharField(
        "Time frame that matches travel",
        max_length=20,
        choices=TIME_FRAME
    )
    FILE_travel = models.FileField(
        "File upload",
        upload_to=None
    )