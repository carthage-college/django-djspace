# -*- coding: utf-8 -*-

from django import forms

from djspace.registration.models.undergraduate import Undergraduate
from djspace.registration.models.graduate import Graduate
from djspace.registration.models.professional import Professional
from djspace.registration.models.professor import Professor
from djspace.registration.models.k12educator import K12Educator
from djspace.registration.models.base_models import YES_NO_DECLINE, RACES
from djspace.registration.models.base_models import UNDERGRADUATE_DEGREE

from djtools.fields import GENDER_CHOICES

from localflavor.us.forms import USPhoneNumberField

class UndergraduateForm(forms.ModelForm):
    """
    A form to collect undergraduate information
    """

    birthdate = forms.DateField(
        label = "Birth date",
        widget=forms.TextInput(attrs={'placeholder': 'Format: 10/31/1993'})
    ),
    gender = forms.TypedChoiceField(
        choices = GENDER_CHOICES, widget = forms.RadioSelect()
    )
    disability = forms.TypedChoiceField(
        choices = YES_NO_DECLINE, widget = forms.RadioSelect()
    )
    race = forms.MultipleChoiceField(
        help_text = 'Check all that apply',
        choices = RACES, widget = forms.CheckboxSelectMultiple()
    )
    degree = forms.TypedChoiceField(
        choices = UNDERGRADUATE_DEGREE, widget = forms.RadioSelect()
    )
    phone = USPhoneNumberField(
        widget=forms.TextInput(attrs={'placeholder': 'eg. 123-456-7890'})
    )

    class Meta:
        model = Undergraduate
        exclude = (
            'salutation', 'maiden', 'additional', 'title_department',
            'webpage', 'street', 'city', 'state', 'ZIP', 'phone',
            'primary', 'primary_other', 'secondary', 'secondary_other',
            'wsgc_school_num', 'wsgc_advisor_salutation', 'wsgc_advisor_first',
            'wsgc_advisor_middle', 'wsgc_advisor_last',
            'wsgc_advisor_title_department', 'wsgc_advisor_email',
            'wsgc_advisor_confirm_email', 'wsgc_advisor_phone',
            'highschool_zip'
        )
        widgets = {
            'citizen': forms.RadioSelect(),
            'rocket_comp': forms.RadioSelect(),
            'webpage': forms.TextInput(attrs={'placeholder': 'eg. www.mywebsite.com'}),
            'graduation': forms.TextInput(attrs={'placeholder': 'eg. 05-15-2014'}),
            #wsgc
            'wsgc_advisor_phone': forms.TextInput(attrs={'placeholder': 'eg. 123-456-7890'}),
            #highschool
            'gpa': forms.TextInput(attrs={'placeholder': 'eg. 3.87'}),
            'CREDITS': forms.TextInput(attrs={'placeholder': 'eg. 86'}),
            #college
            'gpa_major': forms.TextInput(attrs={'placeholder': 'eg. 3.87'}),
            'graduation': forms.TextInput(attrs={'placeholder': 'eg. 05/15'}),
            'year_in_school': forms.TextInput(attrs={'placeholder': 'eg. 2015'})
        }


class GraduateForm(forms.ModelForm):
    """
    A form to collect graduate information
    """

    class Meta:
        model = Graduate
        exclude = (
            'salutation', 'rocket_comp', 'maiden', 'additional',
            'title_department', 'webpage', 'street', 'city', 'state',
            'ZIP', 'primary', 'primary_other', 'secondary', 'secondary_other',
            'wsgc_school_num', 'wsgc_advisor_salutation', 'wsgc_advisor_first',
            'wsgc_advisor_middle', 'wsgc_advisor_last',
            'wsgc_advisor_title_department', 'wsgc_advisor_email',
            'wsgc_advisor_confirm_email'
        )
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

    class Meta:
        model = Professional
        exclude = (
            'salutation', 'maiden', 'additional', 'title_department',
            'webpage', 'secondary', 'secondary_other', 'tribe'
        )
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

    class Meta:
        model = K12Educator
        exclude = (
            'salutation', 'title_department', 'webpage',
            'secondary', 'secondary_other'
        )
        widgets = {
            'webpage': forms.TextInput(attrs={'placeholder': 'eg. www.mywebsite.com'}),
            'phone': forms.TextInput(attrs={'placeholder': 'eg. 123-456-7890'}),
            'birthdate': forms.TextInput(attrs={'placeholder': 'eg. 05-30-1993'}),
            'graduation': forms.TextInput(attrs={'placeholder': '05-15-2014'})
        }
