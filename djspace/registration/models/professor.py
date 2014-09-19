# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import models, connection
from django.contrib.auth.models import User

from djspace.registration.models.base_models import *

class Faculty(BasePersonal):

    campus_email = models.EmailField(
        "Campus email address"
    )
    department_program = models.CharField(
        "Department / Program",
        max_length=128
    )
    title = models.CharField(
        "Title (eg. Assistant Prof., Associate Prof., Prof.)",
        max_length=128
    )
    webpage = models.CharField(
        "Web page",
        max_length=128,
        blank=True
    )
