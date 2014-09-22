# -*- coding: utf-8 -*-

from django import forms

from djspace.registration.models import Undergraduate, Graduate, Faculty
from djspace.registration.models import Professional
from djspace.registration.choices import UNDERGRADUATE_DEGREE, GRADUATE_DEGREE

from djtools.fields import BINARY_CHOICES, YES_NO_DECLINE

class UndergraduateForm(forms.ModelForm):
    """
    A form to collect undergraduate information
    """

    degree = forms.TypedChoiceField(
        choices = UNDERGRADUATE_DEGREE, widget = forms.RadioSelect()
    )

    class Meta:
        model = Undergraduate
        fields = [
            'wsgc_school', 'major',
            'major_other', 'secondary_major_minor',
            'secondary_major_minor_other', 'student_id',
            'current_cumulative_gpa', 'gpa_in_major', 'gpa_scale',
            'cumulative_college_credits',
            'month_year_of_graduation', 'degree',
            'highschool_name', 'highschool_city', 'highschool_state',
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

    degree_program = forms.TypedChoiceField(
        choices = GRADUATE_DEGREE, widget = forms.RadioSelect()
    )

    class Meta:
        model = Graduate
        fields = [
            'wsgc_school', 'degree_program',
            'degree_program_other', 'concentration_area', 'graduate_gpa',
            'graduate_scale', 'graduate_graduation_year',
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
                self._errors["degree_program_other"] = self.error_class(
                    ["Required field."]
                )

        return cleaned_data


class ProfessionalForm(forms.ModelForm):
    """
    A form to collect professional information
    """

    class Meta:
        model = Professional


class FacultyForm(forms.ModelForm):
    """
    A form to collect faculty information
    """

    class Meta:
        model = Faculty
