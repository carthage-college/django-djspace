# -*- coding: utf-8 -*-

from django import forms

from djspace.registration.models.undergraduate import Undergraduate
from djspace.registration.models.graduate import Graduate
from djspace.registration.models.professional import Professional
from djspace.registration.models.professor import Professor
from djspace.registration.models.k12educator import K12Educator

class UndergraduateForm(forms.ModelForm):
    """
    A form to collect undergraduate information
    """

    class Meta:
        model = Undergraduate


class GraduateForm(forms.ModelForm):
    """
    A form to collect graduate information
    """

    class Meta:
        model = Graduate


class ProfessionalForm(forms.ModelForm):
    """
    A form to collect professional information
    """

    class Meta:
        model = Professional


class ProfessorForm(forms.ModelForm):
    """
    A form to collect professor information
    """

    class Meta:
        model = Professor


class K12EducatorForm(forms.ModelForm):
    """
    A form to collect K12 information
    """

    class Meta:
        model = K12Educator
