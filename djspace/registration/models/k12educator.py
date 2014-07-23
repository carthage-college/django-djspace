# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import models, connection
from django.contrib.auth.models import User

from djspace.registration.models.base_models import BasePersonalInformation, BaseEmployerInformation

class K12EducatorInformation(BasePersonalInformation, BaseEmployerInformation):
    
    pass
