# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import models, connection
from django.contrib.auth.models import User

from djspace.registration.models.base_models import *

class Undergraduate(BasePersonal, BaseWSGC, BaseHighschool, BaseUndergrad):

    pass    
    #undergraduate_concentration = models.CharField(
    #    "Area of Undergraduate Concentration in a Space, Aerospace, or Space-Related Field",
    #    max_length=20
    #)
