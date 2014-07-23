# -*- coding: utf-8 -*-

from django import forms

from djspace.registration.models.undergraduate import UndergraduateInformation
from djspace.registration.models.graduate import GraduateInformation
from djspace.registration.models.professional import ProfessionalInformation
from djspace.registration.models.professor import ProfessorInformation
from djspace.registration.models.k12educator import K12EducatorInformation

class UndergraduateInformationForm(forms.ModelForm):
    """
    A form to collect personal information
    """

    class Meta:
        model = UndergraduateInformation

