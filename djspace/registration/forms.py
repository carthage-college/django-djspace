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
    
    def __init__(self, *args, **kwargs):
        super(UndergraduateForm, self).__init__(*args, **kwargs)
        self.fields.pop('salutation')
        self.fields.pop('maiden')
        self.fields.pop('additional')
        self.fields.pop('title_department')
        self.fields.pop('webpage')
        self.fields.pop('street')
        self.fields.pop('city')
        self.fields.pop('state')
        self.fields.pop('ZIP')
        self.fields.pop('phone')
        self.fields.pop('primary')
        self.fields.pop('primary_other')
        self.fields.pop('secondary')
        self.fields.pop('secondary_other')
        self.fields.pop('wsgc_school_num')
        self.fields.pop('wsgc_advisor_salutation')
        self.fields.pop('wsgc_advisor_first')
        self.fields.pop('wsgc_advisor_middle')
        self.fields.pop('wsgc_advisor_last')
        self.fields.pop('wsgc_advisor_title_department')
        self.fields.pop('wsgc_advisor_email')
        self.fields.pop('wsgc_advisor_confirm_email')
        self.fields.pop('wsgc_advisor_phone')
        self.fields.pop('highschool_zip')
    
    class Meta:
        model = Undergraduate
        widgets = {
            'citizen': forms.RadioSelect(),
            'rocket_comp': forms.RadioSelect(),
            'webpage': forms.TextInput(attrs={'placeholder': 'eg. www.mywebsite.com'}),
            'phone': forms.DateInput(attrs={'placeholder': 'eg. 123-456-7890','format':"%m/%d/%Y"}),            
            'birthdate': forms.TextInput(attrs={'placeholder': 'eg. 05/30/1993'}),
            'gender': forms.RadioSelect(),
            'disability': forms.RadioSelect(),
            'race': forms.CheckboxSelectMultiple(attrs={'label':'Check all that apply'}),
            'graduation': forms.TextInput(attrs={'placeholder': 'eg. 05-15-2014'}),
            #wsgc
            'wsgc_advisor_phone': forms.TextInput(attrs={'placeholder': 'eg. 123-456-7890'}),
            #highschool
            'gpa': forms.TextInput(attrs={'placeholder': 'eg. 3.87'}),
            'CREDITS': forms.TextInput(attrs={'placeholder': 'eg. 86'}),
            #college            
            'gpa_major': forms.TextInput(attrs={'placeholder': 'eg. 3.87'}),
            'graduation': forms.TextInput(attrs={'placeholder': 'eg. 05/15'}),
            'degree': forms.RadioSelect(),
            'year_in_school': forms.TextInput(attrs={'placeholder': 'eg. 2015'})
        }


class GraduateForm(forms.ModelForm):
    """
    A form to collect graduate information
    """

    def __init__(self, *args, **kwargs):
        super(GraduateForm, self).__init__(*args, **kwargs)
        self.fields.pop('salutation')
        self.fields.pop('rocket_comp')
        self.fields.pop('maiden')
        self.fields.pop('additional')
        self.fields.pop('title_department')
        self.fields.pop('webpage')
        self.fields.pop('street')
        self.fields.pop('city')
        self.fields.pop('state')
        self.fields.pop('ZIP')
        self.fields.pop('primary')
        self.fields.pop('primary_other')
        self.fields.pop('secondary')
        self.fields.pop('secondary_other')
        self.fields.pop('wsgc_school_num')
        self.fields.pop('wsgc_advisor_salutation')
        self.fields.pop('wsgc_advisor_first')
        self.fields.pop('wsgc_advisor_middle')
        self.fields.pop('wsgc_advisor_last')
        self.fields.pop('wsgc_advisor_title_department')
        self.fields.pop('wsgc_advisor_email')
        self.fields.pop('wsgc_advisor_confirm_email')

    class Meta:
        model = Graduate
        widgets = {
            'webpage': forms.TextInput(attrs={'placeholder': 'eg. www.mywebsite.com'}),
            'phone': forms.TextInput(attrs={'placeholder': 'eg. 123-456-7890'}),
            'race': forms.CheckboxSelectMultiple(attrs={'label':'Check all that apply'}),
            'birthdate': forms.TextInput(attrs={'placeholder': 'eg. 05/30/1993'}),
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
