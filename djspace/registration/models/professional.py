# -*- coding: utf-8 -*-
from django.db import models

from djspace.registration.models.base_models import BasePersonal
from djspace.registration.choices import WSGC_AFFILIATE

class Professional(BasePersonal):

    wsgc_affiliate = models.CharField(
        "WSGC Affiliate",
        max_length=128,
        choices=WSGC_AFFILIATE
    )

