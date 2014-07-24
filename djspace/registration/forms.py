# -*- coding: utf-8 -*-

from django import forms

from djspace.registration.models.undergraduate import UndergraduateInformation
from djspace.registration.models.graduate import GraduateInformation
from djspace.registration.models.professional import ProfessionalInformation
from djspace.registration.models.professor import ProfessorInformation
from djspace.registration.models.k12educator import K12EducatorInformation

class UndergraduateInformationForm(forms.ModelForm):
    """
    A form to collect undergraduate information
    """

    class Meta:
        model = UndergraduateInformation


class GraduateInformationForm(forms.ModelForm):
    """
    A form to collect graduate information
    """
    
    class Meta:
        model = GraduateInformation
        
        
class ProfessionalInformationForm(forms.ModelForm):
    """
    A form to collect professional information
    """
    
    def __init__(self, *args, **kwargs):
        super(ProfessionalInformationForm, self).__init__(*args, **kwargs)
        self.fields.pop('salutation')
        self.fields.pop('maiden')
        self.fields.pop('additional')
        self.fields.pop('title_department')
        self.fields.pop('webpage')
        self.fields.pop('secondary')
        self.fields.pop('secondary_other')
        self.fields.pop('tribe')
    
    class Meta:
        model = ProfessionalInformation
        
        
class ProfessorInformationForm(forms.ModelForm):
    """
    A form to collect professor information
    """
    
    class Meta:
        model = ProfessorInformation
        
        
class K12EducatorInformationForm(forms.ModelForm):
    """
    A form to collect K12 information
    """
    
    def __init__(self, *args, **kwargs):
        super(K12EducatorInformationForm, self).__init__(*args, **kwargs)
        self.fields.pop('salutation')
        self.fields.pop('title_department')
        self.fields.pop('webpage')
        self.fields.pop('secondary')
        self.fields.pop('secondary_other')

    class Meta:
        model = K12EducatorInformation