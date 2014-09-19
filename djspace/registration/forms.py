# -*- coding: utf-8 -*-

from django import forms

from djspace.registration.models.undergraduate import Undergraduate
from djspace.registration.models.graduate import Graduate, GRADUATE_DEGREE
from djspace.registration.models.professional import Professional
from djspace.registration.models.professor import Faculty
from djspace.registration.models.base_models import YES_NO_DECLINE, RACES
from djspace.registration.models.base_models import UNDERGRADUATE_DEGREE

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
    citizen = forms.TypedChoiceField(
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
            'first','middle','last','citizen','birthdate',
            'gender', 'disability','race','tribe','wsgc_school','major',
            'major_other', 'secondary_major_minor',
            'secondary_major_minor_other','student_id', 'gpa',
            'gpa_major','scale', 'CREDITS', 'graduation', 'degree',
            'highschool_name', 'highschool_city', 'highschool_state',
            'address_1', 'address_2', 'city', 'state', 'postal_code', 'phone',
            'email'
        ]
        widgets = {
            'webpage': forms.TextInput(attrs={'placeholder': 'eg. www.mywebsite.com'}),
            'graduation': forms.TextInput(attrs={'placeholder': 'eg. 05/2015'}),
            #wsgc
            'wsgc_advisor_phone': forms.TextInput(attrs={'placeholder': 'eg. 123-456-7890'}),
            #highschool
            'gpa': forms.TextInput(attrs={'placeholder': 'eg. 3.87'}),
            'CREDITS': forms.TextInput(attrs={'placeholder': 'eg. 86.0'}),
            #college
            'scale': forms.TextInput(attrs={'placeholder': 'eg. 4.00'}),
            'gpa_major': forms.TextInput(attrs={'placeholder': 'eg. 3.87'}),
            'graduation': forms.TextInput(attrs={'placeholder': 'eg. 05/2015'}),
            'year_in_school': forms.TextInput(attrs={'placeholder': 'eg. 2015'})
        }

    '''def clean(self):
        cleaned_data = super(UndergraduateForm, self).clean()
        citizen = cleaned_data.get("citizen")

        if citizen == "No":
            self._errors["citizen"] = self.error_class(["Must be Yes."])

        return cleaned_data'''


class GraduateForm(forms.ModelForm):
    """
    A form to collect graduate information
    """

    birthdate = forms.DateField(
        label = "Birth date",
        widget=forms.TextInput(attrs={'placeholder': 'Format: 05/30/1993'})
    )
    citizen = forms.TypedChoiceField(
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
        choices = RACES, widget = forms.CheckboxSelectMultiple()
    )
    degree_program = forms.TypedChoiceField(
        choices = GRADUATE_DEGREE, widget = forms.RadioSelect()
    )

    class Meta:
        model = Graduate
        fields = [
            'first', 'middle', 'last', 'citizen', 'birthdate', 'gender',
            'disability', 'race', 'tribe', 'wsgc_school', 'degree_program',
            'degree_program_other', 'concentration_area', 'graduate_gpa',
            'graduate_scale', 'graduate_graduation_year', 'address_1', 'address_2',
            'city', 'state', 'postal_code', 'phone', 'email'
        ]
        '''exclude = (
            'salutation', 'rocket_comp', 'maiden', 'additional',
            'title_department',
            'primary', 'primary_other', 'secondary',
            'secondary_other', 'wsgc_school_num', 'wsgc_advisor_salutation',
            'wsgc_advisor_first', 'wsgc_advisor_middle', 'wsgc_advisor_last',
            'wsgc_advisor_title_department', 'wsgc_advisor_email',
            'wsgc_advisor_confirm_email'
        )'''
        widgets = {
            'webpage': forms.TextInput(attrs={'placeholder': 'eg. www.mywebsite.com'}),
            'phone': forms.TextInput(attrs={'placeholder': 'eg. 123-456-7890'}),
            'birthdate': forms.TextInput(attrs={'placeholder': 'eg. 05/30/1993'}),
            'graduation': forms.TextInput(attrs={'placeholder': '05-15-2014'}),
            #wsgc
            'wsgc_advisor_phone': forms.TextInput(attrs={'placeholder': 'eg. 123-456-7890'}),
            #college
            'graduate_gpa': forms.TextInput(attrs={'placeholder': 'eg. 3.87'}),
            'graduate_gpa_major': forms.TextInput(attrs={'placeholder': 'eg. 3.87'}),
            'graduate_CREDITS': forms.TextInput(attrs={'placeholder': 'eg. 86'}),
            'graduate_scale': forms.TextInput(attrs={'placeholder': 'eg. 4.00'}),
            'graduate_year_in_school': forms.TextInput(attrs={'placeholder': 'eg. 2015'}),
            'graduate_graduation': forms.TextInput(attrs={'placeholder': 'eg. 05-15-2014'}),
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
        choices = RACES, widget = forms.CheckboxSelectMultiple()
    )

    class Meta:
        model = Professional
        fields = [
            'first', 'middle', 'last', 'citizen', 'birthdate',
            'gender','disability','race', 'wsgc_affiliate',
            'phone', 'email'
        ]
        exclude = (
            'salutation', 'maiden', 'additional', 'title_department',
            'webpage', 'secondary', 'secondary_other', 'tribe'
        )
        widgets = {
            'citizen': forms.RadioSelect(),
            'webpage': forms.TextInput(attrs={'placeholder': 'eg. www.mywebsite.com'}),
            'phone': forms.TextInput(attrs={'placeholder': 'eg. 123-456-7890'}),
            'birthdate': forms.TextInput(attrs={'placeholder': 'eg. 05-30-1993'}),
            'graduation': forms.TextInput(attrs={'placeholder': '05-15-2014'})
        }


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
        choices = RACES, widget = forms.CheckboxSelectMultiple()
    )
    #campus_phone = USPhoneNumberField(
    #    "Campus phone number",
    #    widget=forms.TextInput(attrs={'placeholder': 'eg. 123-456-7890'})
    #)

    class Meta:
        model = Faculty
        fields = [
            'salutation', 'first', 'middle', 'last', 'gender', 'disability',
            'race', 'tribe', 'citizen', 'department_program', 'title',
            'webpage', 'campus_email', 'address_1', 'address_2', 'city',
            'state', 'postal_code',
            #'campus_phone'
        ]
        widgets = {
            'citizen': forms.RadioSelect(),
            'webpage': forms.TextInput(attrs={'placeholder': 'eg. www.mywebsite.com'}),
            'phone': forms.TextInput(attrs={'placeholder': 'eg. 123-456-7890'}),
            'birthdate': forms.TextInput(attrs={'placeholder': 'eg. 05-30-1993'}),
            'graduation': forms.TextInput(attrs={'placeholder': '05-15-2014'})
        }