# -*- coding: utf-8 -*-

from django import forms

from djspace.registration.models import PersonalInformation


class PersonalInformationForm(forms.ModelForm):
    """
    A form to collect personal information
    """

    class Meta:
        model = PersonalInformation