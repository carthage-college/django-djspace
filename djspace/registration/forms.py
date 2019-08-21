# -*- coding: utf-8 -*-

from django import forms

from djspace.core.models import GenericChoice
from djspace.registration.models import (
    HighSchool, Undergraduate, Graduate, Faculty, GrantsOfficer, Professional
)
from djspace.registration.choices import UNDERGRADUATE_DEGREE, GRADUATE_DEGREE

from djtools.fields import STATE_CHOICES
from djtools.fields.localflavor import USPhoneNumberField
#from djtools.fields.validators import month_year_validator

from localflavor.us.forms import USZipCodeField

try:
    AFFILIATES = GenericChoice.objects.filter(
        tags__name__in=['WSGC Affiliates','College or University']
    ).filter(active=True).order_by('ranking','name')
except:
    AFFILIATES = GenericChoice.objects.none()


class HighSchoolForm(forms.ModelForm):
    """
    A form for high school registrants
    """

    class Meta:
        model = HighSchool
        exclude = ('user','date_created','date_updated','updated_by')


class UndergraduateForm(forms.ModelForm):
    """
    A form to collect undergraduate information
    """

    def __init__(self, *args, **kwargs):
        super(UndergraduateForm, self).__init__(*args, **kwargs)
        self.fields['wsgc_affiliate'].queryset = GenericChoice.objects.filter(
            tags__name__in=['College or University']
        ).order_by('ranking','name')

    class Meta:
        model = Undergraduate
        exclude = ('user','status',)
        fields = [
            'wsgc_affiliate', 'wsgc_affiliate_other', 'studentid',
            'class_year', 'major', 'major_other', 'secondary_major_minor',
            'secondary_major_minor_other', 'current_cumulative_gpa',
            'gpa_in_major', 'gpa_scale', 'cumulative_college_credits',
            'month_year_of_graduation', 'highschool_name',
            'highschool_city', 'highschool_state','cv','cv_authorize'
        ]
        widgets = {
            'current_cumulative_gpa': forms.TextInput(
                attrs={'placeholder': 'eg. 3.87'}
            ),
            'gpa_in_major': forms.TextInput(attrs={'placeholder': 'eg. 3.87'}),
            'gpa_scale': forms.TextInput(attrs={'placeholder': 'eg. 4.00'}),
            'cumulative_college_credits': forms.TextInput(
                attrs={'placeholder': 'eg. 86.0'}
            ),
            'month_year_of_graduation': forms.TextInput(
                attrs={'placeholder': 'eg. 05/2015'}
            )
        }

    def clean(self):
        cleaned_data = self.cleaned_data

        # WSGC Affiliate
        wsgc_affiliate = cleaned_data.get('wsgc_affiliate')
        wsgc_affiliate_other = cleaned_data.get('wsgc_affiliate_other')

        if wsgc_affiliate == 'Other' and not wsgc_affiliate_other:
            self._errors['wsgc_affiliate_other'] = self.error_class(
                ["Required field."]
            )

        # majors
        major = cleaned_data.get('major')
        major_other = cleaned_data.get('major_other')
        secondary_major_minor = cleaned_data.get('secondary_major_minor')
        secondary_major_minor_other = cleaned_data.get(
            'secondary_major_minor_other'
        )

        if major == 'Other':
            if major_other == '':
                self._errors['major_other'] = self.error_class(
                    ["Required field."]
                )

        if secondary_major_minor == 'Other':
            if secondary_major_minor_other == '':
                self._errors['secondary_major_minor_other'] = self.error_class(
                    ["Required field."]
                )

        return cleaned_data


class GraduateForm(forms.ModelForm):
    """
    A form to collect graduate information
    """

    def __init__(self, *args, **kwargs):
        super(GraduateForm, self).__init__(*args, **kwargs)
        self.fields['wsgc_affiliate'].queryset = GenericChoice.objects.filter(
            tags__name__in=['College or University']
        ).order_by('ranking','name')


    cumulative_college_credits = forms.CharField(
        label = "Total credits"
    )
    month_year_of_graduation = forms.CharField(
        label = "Month and year of graduation",
        max_length=7,
        widget=forms.TextInput(attrs={'placeholder': 'eg. 05/2015'}),
        #validators=[month_year_validator]
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
            'major', 'major_other','secondary_major_minor',
            'secondary_major_minor_other',
            'gpa_in_major','gpa_scale','cumulative_college_credits',
            'month_year_of_graduation','undergraduate_degree',
            'wsgc_affiliate','wsgc_affiliate_other','studentid',
            'degree_program','degree_program_other',
            'concentration_area','graduate_gpa',
            'graduate_scale','graduate_graduation_year','cv','cv_authorize'
        ]
        widgets = {
            # undergraduate
            'gpa_in_major': forms.TextInput(attrs={'placeholder': 'eg. 3.87'}),
            'gpa_scale': forms.TextInput(attrs={'placeholder': 'eg. 4.00'}),
            'cumulative_college_credits': forms.TextInput(
                attrs={'placeholder': 'eg. 86.0'}
            ),
            # graduate
            'graduate_gpa': forms.TextInput(attrs={'placeholder': 'eg. 3.87'}),
            'graduate_scale': forms.TextInput(
                attrs={'placeholder': 'eg. 4.00'}
            ),
            'graduate_graduation_year': forms.TextInput(
                attrs={'placeholder': 'eg. 2015'}
            )
        }

    def clean(self):
        cleaned_data = self.cleaned_data

        # WSGC Affiliate
        wsgc_affiliate = cleaned_data.get('wsgc_affiliate')
        wsgc_affiliate_other = cleaned_data.get('wsgc_affiliate_other')

        if wsgc_affiliate == 'Other' and not wsgc_affiliate_other:
            self._errors['wsgc_affiliate_other'] = self.error_class(
                ["Required field."]
            )

        # majors
        major = cleaned_data.get('major')
        major_other = cleaned_data.get('major_other')
        secondary_major_minor = cleaned_data.get('secondary_major_minor')
        secondary_major_minor_other = cleaned_data.get(
            'secondary_major_minor_other'
        )
        degree_program = cleaned_data.get('degree_program')
        degree_program_other = cleaned_data.get('degree_program_other')

        if major == 'Other':
            if major_other == '':
                self._errors['major_other'] = self.error_class(
                    ["Required field."]
                )

        if secondary_major_minor == 'Other':
            if secondary_major_minor_other == '':
                self._errors['secondary_major_minor_other'] = self.error_class(
                    ["Required field."]
                )

        if degree_program == 'Other':
            if degree_program_other == '':
                self._errors['degree_program_other'] = self.error_class(
                    ["Required field."]
                )
        return cleaned_data


class ProfessionalForm(forms.ModelForm):
    """
    A form to collect professional information
    """

    wsgc_affiliate = forms.ModelChoiceField(
        label = "WSGC Affiliate",
        queryset=AFFILIATES
    )
    sponsoring_organization_state = forms.CharField(
        required=False,
        widget=forms.Select(choices=STATE_CHOICES)
    )
    sponsoring_organization_postal_code = USZipCodeField(
        label="Zip Code",
        help_text="Format: 99999 or 99999-9999",
        required=False,
        max_length=10
    )

    class Meta:
        model = Professional
        exclude = ('user','status',)

    def clean(self):
        cd = self.cleaned_data
        wa = cd.get('wsgc_affiliate')
        # sponsoring organisation data are required if wsgc affiliate
        # is "Other" (id = 49)
        if wa and wa.id == 49:
            if not cd.get('sponsoring_organization_name'):
                self._errors['sponsoring_organization_name'] = self.error_class(
                    ["Required field"]
                )
            if not cd.get('sponsoring_organization_address1'):
                self._errors['sponsoring_organization_address1'] = self.error_class(
                    ["Required field"]
                )
            if not cd.get('sponsoring_organization_city'):
                self._errors['sponsoring_organization_city'] = self.error_class(
                    ["Required field"]
                )
            if not cd.get('sponsoring_organization_state'):
                self._errors['sponsoring_organization_state'] = self.error_class(
                    ["Required field"]
                )
            if not cd.get('sponsoring_organization_postal_code'):
                self._errors['sponsoring_organization_postal_code'] = self.error_class(
                    ["Required field"]
                )
            if not cd.get('sponsoring_organization_contact'):
                self._errors['sponsoring_organization_contact'] = self.error_class(
                    ["Required field"]
                )
        return cd


class FacultyForm(forms.ModelForm):
    """
    A form to collect faculty information
    """

    wsgc_affiliate = forms.ModelChoiceField(
        label = "WSGC Affiliate",
        queryset=AFFILIATES
    )

    class Meta:
        model = Faculty
        exclude = ('user','status',)

    def clean(self):
        cleaned_data = self.cleaned_data

        # WSGC Affiliate
        wsgc_affiliate = cleaned_data.get('wsgc_affiliate')
        wsgc_affiliate_other = cleaned_data.get('wsgc_affiliate_other')

        if wsgc_affiliate.name == 'Other' and not wsgc_affiliate_other:
            self._errors['wsgc_affiliate_other'] = self.error_class(
                ["Required field."]
            )

        return cleaned_data


class GrantsOfficerForm(forms.ModelForm):
    """
    A form to collect grants officer information
    """

    wsgc_affiliate = forms.ModelChoiceField(
        label = "WSGC Affiliate",
        queryset=AFFILIATES
    )

    class Meta:
        model = GrantsOfficer
        exclude = ('user','status',)

    def clean(self):
        cleaned_data = self.cleaned_data

        # WSGC Affiliate
        wsgc_affiliate = cleaned_data.get('wsgc_affiliate')
        wsgc_affiliate_other = cleaned_data.get('wsgc_affiliate_other')

        if wsgc_affiliate.name == 'Other' and not wsgc_affiliate_other:
            self._errors['wsgc_affiliate_other'] = self.error_class(
                ["Required field."]
            )

        return cleaned_data
