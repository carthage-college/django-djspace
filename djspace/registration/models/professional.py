# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import models, connection
from django.contrib.auth.models import User

from djspace.registration.models.base_models import *

class Professional(BasePersonal, BaseEmployer):
    
    wsgc_affiliate = models.CharField(
        "WSGC Affiliate",
        max_length=128,
        choices=WSGC_AFFILIATE
    )

