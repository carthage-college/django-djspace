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
        widgets = {
            'webpage': forms.TextInput(attrs={'placeholder': 'eg. www.mywebsite.com'}),
            'phone': forms.TextInput(attrs={'placeholder': 'eg. 123-456-7890'}),            
            'birthdate': forms.TextInput(attrs={'placeholder': 'eg. 05-30-1993'}),
            'graduation': forms.TextInput(attrs={'placeholder': 'eg. 05-15-2014'}),
            #wsgc
            'wsgc_advisor_phone': forms.TextInput(attrs={'placeholder': 'eg. 123-456-7890'}),
            #highschool
            'gpa': forms.TextInput(attrs={'placeholder': 'eg. 3.87'}),
            'CREDITS': forms.TextInput(attrs={'placeholder': 'eg. 86'}),
            #college
            'gpa_major': forms.TextInput(attrs={'placeholder': 'eg. 3.87'}),
            'year_in_school': forms.TextInput(attrs={'placeholder': 'eg. 2015'})
        }


class GraduateForm(forms.ModelForm):
    """
    A form to collect graduate information
    """

    class Meta:
        model = Graduate
        widgets = {
            'webpage': forms.TextInput(attrs={'placeholder': 'eg. www.mywebsite.com'}),
            'phone': forms.TextInput(attrs={'placeholder': 'eg. 123-456-7890'}),            
            'birthdate': forms.TextInput(attrs={'placeholder': 'eg. 05-30-1993'}),
            'graduation': forms.TextInput(attrs={'placeholder': '05-15-2014'}),
            #wsgc
            'wsgc_advisor_phone': forms.TextInput(attrs={'placeholder': 'eg. 123-456-7890'}),
            #college
            'graduate_gpa': forms.TextInput(attrs={'placeholder': 'eg. 3.87'}),
            'graduate_gpa_major': forms.TextInput(attrs={'placeholder': 'eg. 3.87'}),
            'graduate_CREDITS': forms.TextInput(attrs={'placeholder': 'eg. 86'}),
            'graduate_year_in_school': forms.TextInput(attrs={'placeholder': 'eg. 2015'}),
            'graduate_graduation': forms.TextInput(attrs={'placeholder': 'eg. 05-15-2014'})
        }


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
        widgets = {
            'webpage': forms.TextInput(attrs={'placeholder': 'eg. www.mywebsite.com'}),
            'phone': forms.TextInput(attrs={'placeholder': 'eg. 123-456-7890'}),            
            'birthdate': forms.TextInput(attrs={'placeholder': 'eg. 05-30-1993'}),
            'graduation': forms.TextInput(attrs={'placeholder': '05-15-2014'})
        }


class ProfessorForm(forms.ModelForm):
    """
    A form to collect professor information
    """

    class Meta:
        model = Professor
        widgets = {
            'webpage': forms.TextInput(attrs={'placeholder': 'eg. www.mywebsite.com'}),
            'phone': forms.TextInput(attrs={'placeholder': 'eg. 123-456-7890'}),            
            'birthdate': forms.TextInput(attrs={'placeholder': 'eg. 05-30-1993'}),
            'graduation': forms.TextInput(attrs={'placeholder': '05-15-2014'})
        }


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
        widgets = {
            'webpage': forms.TextInput(attrs={'placeholder': 'eg. www.mywebsite.com'}),
            'phone': forms.TextInput(attrs={'placeholder': 'eg. 123-456-7890'}),            
            'birthdate': forms.TextInput(attrs={'placeholder': 'eg. 05-30-1993'}),
            'graduation': forms.TextInput(attrs={'placeholder': '05-15-2014'})
        }
