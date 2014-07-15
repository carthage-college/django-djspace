# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import models, connection
from django.contrib.auth.models import User

"""
Model: ...
"""

class MyModel(models.Model):
    created_by          = models.ForeignKey(
        User,verbose_name="Created by",
        related_name="created_by",editable=False,null=True,blank=True
    )
    updated_by          = models.ForeignKey(
        User,verbose_name="Updated by",
        related_name="updated_by",editable=False,null=True,blank=True
    )
    created_at          = models.DateTimeField(
        "Date Created",auto_now_add=True
    )
    updated_at          = models.DateTimeField(
        "Date Updated",auto_now=True
    )

    class Meta:
        ordering  = ['-created_at']
        get_latest_by = 'created_at'

    def __unicode__(self):
        """
        Default data for display
        """
        return self.created_by.username

    @models.permalink
    def get_absolute_url(self):
        return ('myapp_detail', [str(self.id)])
        
        

class PersonalInformation(models.Model):
    
    rocket_contest = models.BooleanField()
    
    DEF_CITIZEN = "df"
    US = "y"
    NON_US = "n"
    CITIZENSHIP_CHOICES = (
        (DEF_CITIZEN, "Pick One"),
        (US, "Yes"),
        (NON_US, "No"),
    )
    citizenship = models.CharField(max_length=2,choices=CITIZENSHIP_CHOICES,default=DEF_CITIZEN)
    
    DEF_PROFESSION = "df"
    UNDERGRAD = "undg"
    GRADUATE = "grad"
    PROFESSIONAL = "prfs"
    PROFESSOR = "prof"
    K12_EDUCATOR = "k12"
    PROFESSION_CHOICES = (
        (DEF_PROFESSION,"Pick One"),
        (UNDERGRAD,"Undergrad"),
        (GRADUATE,"Graduate"),
        (PROFESSIONAL,"Professional"),
        (PROFESSOR,"Professor"),
        (K12_EDUCATOR,"K12 Educator"),
    )
    profession = models.CharField(max_length=4,choices=PROFESSION_CHOICES,default=DEF_PROFESSION)
    
    DEF_SALUTATION = "df"
    MR = "mr"
    MS = "ms"
    MRS = "mrs"
    DR = "dr"
    SALUTATION_CHOICES = (
        (DEF_SALUTATION,"Pick One"),
        (MR,'Mr'),
        (MS,'Ms'),
        (MRS,'Mrs'),
        (DR,'Dr'),
    )
    salutation = models.CharField(max_length=3,choices=SALUTATION_CHOICES,default=DEF_SALUTATION)
    
    first = models.CharField(max_length=20)
    middle = models.CharField(max_length=15)
    last = models.CharField(max_length=20)
    maiden_name = models.CharField(max_length=20)
    additional_name = models.CharField(max_length=20)
    title_department = models.CharField("Title or Department",max_length=40)
    web_page = models.CharField(max_length=50)
    
    
