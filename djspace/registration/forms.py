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

    def __init__(self, *args, **kwargs):
        super(ProfessionalForm, self).__init__(*args, **kwargs)
        self.fields.pop('salutation')
        self.fields.pop('maiden')
        self.fields.pop('additional')
        self.fields.pop('title_department')
        self.fields.pop('webpage')
        self.fields.pop('secondary')
        self.fields.pop('secondary_other')
        self.fields.pop('tribe')

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

    def __init__(self, *args, **kwargs):
        super(K12EducatorForm, self).__init__(*args, **kwargs)
        self.fields.pop('salutation')
        self.fields.pop('title_department')
        self.fields.pop('webpage')
        self.fields.pop('secondary')
        self.fields.pop('secondary_other')

    class Meta:
        model = K12Educator
