# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import models, connection
from django.contrib.auth.models import User

from djspace.registration.models.base_models import *

class ProfessionalInformation(BasePersonalInformation, BaseEmployerInformation):
    
    # remove fields:
    """
        salutation
        maiden
        additional_name
        title_department
        web_page
        secondary
        secondary_other
        tribe
    """
    pass