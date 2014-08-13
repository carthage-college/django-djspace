# -*- coding: utf-8 -*-

from django import forms

from djspace.application.models import *

class UndergraduateForm(forms.ModelForm):
    """
    A form to collect undergraduate information
    """

    class Meta:
        model = Student


class GraduateForm(forms.ModelForm):
    """
    A form to collect graduate information
    """

    class Meta:
        model = Student


class ProfessionalForm(forms.ModelForm):
    """
    A form to collect professional information
    """

    class Meta:
        model = NonEducator


class ProfessorForm(forms.ModelForm):
    """
    A form to collect professor information
    """

    class Meta:
        model = NonEducator
