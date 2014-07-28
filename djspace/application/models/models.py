 # -*- coding: utf-8 -*-
from django.conf import settings
from django.db import models, connection
from django.contrib.auth.models import User

from djspace.application.models.base_models import *

# This class handles both undergraduate and graduate
# because both are the same
class Student(BaseFacultyAdvisor, StudentTravel):
    
    pass


# This class handles both professional and professor
# because both are the same
class NonEducator(BaseFacultyAdvisor):
    
    pass


# K12 Educators cannot take this form