# -*- coding: utf-8 -*-

from django import forms

from djspace.registration.models import PersonalInformation, AddressInformation


class PersonalInformationForm(forms.ModelForm):
    """
    A form to collect personal information
    """

    class Meta:
        model = PersonalInformation
        


class AddressInformationForm(forms.ModelForm):
    """
    A form to collect address information
    """
    
    class Meta:
        model = AddressInformation