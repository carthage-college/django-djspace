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
    
    class Meta:
        model = K12EducatorInformation