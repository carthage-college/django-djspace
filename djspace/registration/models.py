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
