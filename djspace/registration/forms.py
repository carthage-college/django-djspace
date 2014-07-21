# -*- coding: utf-8 -*-

from django import forms

from djspace.registration.models import *


class UndergraduateInformationForm(forms.ModelForm):
    """
    A form to collect personal information
    """

    class Meta:
        model = UndergraduateInformation
        