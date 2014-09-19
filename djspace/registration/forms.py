# -*- coding: utf-8 -*-

from django import forms

from djspace.registration.models.undergraduate import *
from djspace.registration.models.graduate import Graduate
from djspace.registration.models.professional import Professional
from djspace.registration.models.professor import Faculty
from djspace.registration.choices import YES_NO_DECLINE, RACES, GRADUATE_DEGREE

from djtools.fields import GENDER_CHOICES, BINARY_CHOICES, SALUTATION_TITLES

from localflavor.us.forms import USPhoneNumberField

class UndergraduateForm(forms.ModelForm):
    """
    A form to collect undergraduate information
    """

    birthdate = forms.DateField(
        label = "Birth date",
        widget=forms.TextInput(attrs={'placeholder': 'Format: 05/30/1993'})
    )
    us_citizen = forms.TypedChoiceField(
        choices = BINARY_CHOICES, widget = forms.RadioSelect()
    )
    gender = forms.TypedChoiceField(
        choices = GENDER_CHOICES, widget = forms.RadioSelect()
    )
    disability = forms.TypedChoiceField(
        choices = YES_NO_DECLINE, widget = forms.RadioSelect()
    )
    race = forms.MultipleChoiceField(
        help_text = 'Check all that apply',
        choices = RACES,
        widget = forms.CheckboxSelectMultiple()
    )
    degree = forms.TypedChoiceField(
        choices = UNDERGRADUATE_DEGREE, widget = forms.RadioSelect()
    )
    phone = USPhoneNumberField(
        widget=forms.TextInput(attrs={'placeholder': 'eg. 123-456-7890'})
    )

    class Meta:
        model = Undergraduate
        fields = [
            'first_name', 'middle_initial', 'last_name', 'us_citizen', 'birthdate',
            'gender', 'disability', 'race', 'tribe', 'wsgc_school', 'major',
            'major_other', 'secondary_major_minor', 'secondary_major_minor_other', 'student_id',
            'current_cumulative_gpa', 'gpa_in_major', 'gpa_scale', 'cumulative_college_credits',
            'month_year_of_graduation', 'degree',
            'highschool_name', 'highschool_city', 'highschool_state',
            'address_1', 'address_2', 'city', 'state', 'postal_code', 'phone', 'email'
        ]
        widgets = {
            'current_cumulative_gpa': forms.TextInput(attrs={'placeholder': 'eg. 3.87'}),
            'gpa_in_major': forms.TextInput(attrs={'placeholder': 'eg. 3.87'}),
            'gpa_scale': forms.TextInput(attrs={'placeholder': 'eg. 4.00'}),
            'cumulative_college_credits': forms.TextInput(attrs={'placeholder': 'eg. 86.0'}),
            'month_year_of_graduation': forms.TextInput(attrs={'placeholder': 'eg. 05/2015'})
        }



class GraduateForm(forms.ModelForm):
    """
    A form to collect graduate information
    """

    birthdate = forms.DateField(
        label = "Birth date",
        widget=forms.TextInput(attrs={'placeholder': 'Format: 05/30/1993'})
    )
    us_citizen = forms.TypedChoiceField(
        choices = BINARY_CHOICES, widget = forms.RadioSelect()
    )
    gender = forms.TypedChoiceField(
        choices = GENDER_CHOICES, widget = forms.RadioSelect()
    )
    disability = forms.TypedChoiceField(
        choices = YES_NO_DECLINE, widget = forms.RadioSelect()
    )
    race = forms.MultipleChoiceField(
        help_text = 'Check all that apply',
        choices = RACES,
        widget = forms.CheckboxSelectMultiple()
    )
    degree_program = forms.TypedChoiceField(
        choices = GRADUATE_DEGREE, widget = forms.RadioSelect()
    )
    phone = USPhoneNumberField(
        widget=forms.TextInput(attrs={'placeholder': 'eg. 123-456-7890'})
    )

    class Meta:
        model = Graduate
        fields = [
            'first_name', 'middle_initial', 'last_name', 'us_citizen', 'birthdate', 'gender',
            'disability', 'race', 'tribe', 'wsgc_school', 'degree_program',
            'degree_program_other', 'concentration_area', 'graduate_gpa',
            'graduate_scale', 'graduate_graduation_year',
            'address_1', 'address_2', 'city', 'state', 'postal_code', 'phone', 'email'
        ]
        widgets = {
            #college
            'graduate_gpa': forms.TextInput(attrs={'placeholder': 'eg. 3.87'}),
            'graduate_scale': forms.TextInput(attrs={'placeholder': 'eg. 4.00'}),
            'graduate_graduation_year': forms.TextInput(attrs={'placeholder': 'eg. 2015'})
        }

    def clean(self):
        cleaned_data = super(GraduateForm, self).clean()
        degree_program = cleaned_data.get("degree_program")
        degree_program_other = cleaned_data.get("degree_program_other")

        if degree_program == "Other":
            if degree_program_other == "":
                self._errors["degree_program_other"] = self.error_class(["Required field."])

        return cleaned_data


class ProfessionalForm(forms.ModelForm):
    """
    A form to collect professional information
    """

    us_citizen = forms.TypedChoiceField(
        choices = BINARY_CHOICES, widget = forms.RadioSelect()
    )
    birthdate = forms.DateField(
        label = "Birth date",
        widget=forms.TextInput(attrs={'placeholder': 'Format: 05/30/1993'})
    )
    gender = forms.TypedChoiceField(
        choices = GENDER_CHOICES, widget = forms.RadioSelect()
    )
    disability = forms.TypedChoiceField(
        choices = YES_NO_DECLINE, widget = forms.RadioSelect()
    )
    race = forms.MultipleChoiceField(
        help_text = 'Check all that apply',
        choices = RACES,
        widget = forms.CheckboxSelectMultiple()
    )
    phone = USPhoneNumberField(
        widget=forms.TextInput(attrs={'placeholder': 'eg. 123-456-7890'})
    )

    class Meta:
        model = Professional
        fields = [
            'first_name', 'middle_initial', 'last_name', 'us_citizen', 'birthdate',
            'gender','disability','race', 'wsgc_affiliate',
            'phone', 'email'
        ]


class FacultyForm(forms.ModelForm):
    """
    A form to collect faculty information
    """

    salutation = forms.CharField(
        widget=forms.Select(choices=SALUTATION_TITLES),
        required=False
    )
    gender = forms.TypedChoiceField(
        choices = GENDER_CHOICES, widget = forms.RadioSelect()
    )
    disability = forms.TypedChoiceField(
        choices = YES_NO_DECLINE, widget = forms.RadioSelect()
    )
    race = forms.MultipleChoiceField(
        help_text = 'Check all that apply',
        choices = RACES,
        widget = forms.CheckboxSelectMultiple()
    )
    us_citizen = forms.TypedChoiceField(
        choices = BINARY_CHOICES, widget = forms.RadioSelect()
    )
    #campus_phone = USPhoneNumberField(
    #    "Campus phone number",
    #    widget=forms.TextInput(attrs={'placeholder': 'eg. 123-456-7890'})
    #)

    class Meta:
        model = Faculty
        fields = [
            'salutation', 'first_name', 'middle_initial', 'last_name', 'gender', 'disability',
            'race', 'tribe', 'us_citizen', 'department_program', 'title',
            'webpage', 'campus_email', 'address_1', 'address_2', 'city',
            'state', 'postal_code', #'campus_phone'
        ]
        widgets = {
            'webpage': forms.TextInput(attrs={'placeholder': 'eg. www.mywebsite.com'})
        }
