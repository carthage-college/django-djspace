# -*- coding: utf-8 -*-

from djspace.registration.models.base_models import BasePersonal

class Professional(BasePersonal):

    wsgc_affiliate = models.CharField(
        "WSGC Affiliate",
        max_length=128,
        choices=WSGC_AFFILIATE
    )

