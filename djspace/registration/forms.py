# -*- coding: utf-8 -*-

from django import forms

from djspace.core.models import GenericChoice
from djspace.registration.models import Professional
from djspace.registration.models import Undergraduate, Graduate, Faculty
from djspace.registration.choices import UNDERGRADUATE_DEGREE, GRADUATE_DEGREE

from djtools.fields import BINARY_CHOICES, YES_NO_DECLINE
from djtools.fields.validators import month_year_validator

try:
    AFFILIATES = GenericChoice.objects.filter(tags__name__in=["WSGC Affiliates"]).order_by("name")
except:
    AFFILIATES = GenericChoice.objects.none()

class UndergraduateForm(forms.ModelForm):
    """
    A form to collect undergraduate information
    """

    class Meta:
        model = Undergraduate
        exclude = ('user','status',)
        fields = [
            'wsgc_school', 'major',
            'major_other', 'secondary_major_minor',
            'secondary_major_minor_other', 'current_cumulative_gpa',
            'gpa_in_major', 'gpa_scale', 'cumulative_college_credits',
            'month_year_of_graduation', 'highschool_name',
            'highschool_city', 'highschool_state',
        ]
        widgets = {
            'current_cumulative_gpa': forms.TextInput(attrs={'placeholder': 'eg. 3.87'}),
            'gpa_in_major': forms.TextInput(attrs={'placeholder': 'eg. 3.87'}),
            'gpa_scale': forms.TextInput(attrs={'placeholder': 'eg. 4.00'}),
            'cumulative_college_credits': forms.TextInput(attrs={'placeholder': 'eg. 86.0'}),
            'month_year_of_graduation': forms.TextInput(attrs={'placeholder': 'eg. 05/2015'})
        }

    def clean(self):
        cleaned_data = super(UndergraduateForm, self).clean()
        major = cleaned_data.get("major")
        major_other = cleaned_data.get("major_other")
        secondary_major_minor = cleaned_data.get("secondary_major_minor")
        secondary_major_minor_other = cleaned_data.get("secondary_major_minor_other")

        if major == "Other":
            if major_other == "":
                self._errors["major_other"] = self.error_class(
                    ["Required field."]
                )

        if secondary_major_minor == "Other":
            if secondary_major_minor_other == "":
                self._errors["secondary_major_minor_other"] = self.error_class(
                    ["Required field."]
                )

        return cleaned_data


class GraduateForm(forms.ModelForm):
    """
    A form to collect graduate information
    """

    cumulative_college_credits = forms.CharField(
        label = "Total credits"
    )
    month_year_of_graduation = forms.CharField(
        label = "Month and year of graduation",
        max_length=7,
        validators=[month_year_validator],
        widget=forms.TextInput(attrs={'placeholder': 'eg. 05/2015'})
    )
    undergraduate_degree = forms.TypedChoiceField(
        choices = UNDERGRADUATE_DEGREE, widget = forms.RadioSelect()
    )
    degree_program = forms.TypedChoiceField(
        label = "Graduate degree program",
        choices = GRADUATE_DEGREE, widget = forms.RadioSelect()
    )

    class Meta:
        model = Graduate
        exclude = ('user','status',)
        fields = [
            'major',
            'major_other', 'secondary_major_minor',
            'secondary_major_minor_other',
            'gpa_in_major', 'gpa_scale', 'cumulative_college_credits',
            'month_year_of_graduation', 'undergraduate_degree',
            'wsgc_school', 'degree_program', 'degree_program_other',
            'concentration_area', 'graduate_gpa',
            'graduate_scale', 'graduate_graduation_year',
        ]
        widgets = {
            # undergraduate
            'gpa_in_major': forms.TextInput(attrs={'placeholder': 'eg. 3.87'}),
            'gpa_scale': forms.TextInput(attrs={'placeholder': 'eg. 4.00'}),
            'cumulative_college_credits': forms.TextInput(attrs={'placeholder': 'eg. 86.0'}),
            # graduate
            'graduate_gpa': forms.TextInput(attrs={'placeholder': 'eg. 3.87'}),
            'graduate_scale': forms.TextInput(attrs={'placeholder': 'eg. 4.00'}),
            'graduate_graduation_year': forms.TextInput(attrs={'placeholder': 'eg. 2015'})
        }

    def clean(self):
        cleaned_data = super(GraduateForm, self).clean()
        major = cleaned_data.get("major")
        major_other = cleaned_data.get("major_other")
        secondary_major_minor = cleaned_data.get("secondary_major_minor")
        secondary_major_minor_other = cleaned_data.get("secondary_major_minor_other")
        degree_program = cleaned_data.get("degree_program")
        degree_program_other = cleaned_data.get("degree_program_other")

        if major == "Other":
            if major_other == "":
                self._errors["major_other"] = self.error_class(
                    ["Required field."]
                )

        if secondary_major_minor == "Other":
            if secondary_major_minor_other == "":
                self._errors["secondary_major_minor_other"] = self.error_class(
                    ["Required field."]
                )

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

    wsgc_affiliate = forms.ModelChoiceField(queryset=AFFILIATES)

    class Meta:
        model = Professional
        exclude = ('user','status',)


class FacultyForm(forms.ModelForm):
    """
    A form to collect faculty information
    """

    class Meta:
        model = Faculty
        exclude = ('user','status',)
