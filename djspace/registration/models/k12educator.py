# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import models, connection
from django.contrib.auth.models import User

from djspace.registration.models.base_models import *

<<<<<<< HEAD
class K12Educator(BasePersonal, BaseEmployer):

=======
class K12EducatorInformation(BasePersonalInformation, BaseEmployerInformation):
    
    # fields to remove
    """
        salutation
        additional (RENAME TO "Nickname")
        title
        webpage
        secondary
        secondary_other
        
    """
    
>>>>>>> 03189e61af75450444ee49681e4742300730b54c
    pass
