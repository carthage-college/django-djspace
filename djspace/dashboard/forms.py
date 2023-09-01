# -*- coding: utf-8 -*-

from django import forms
from djspace.core.models import BIRTH_YEAR_CHOICES
from djspace.core.models import DISABILITY_CHOICES
from djspace.core.models import REG_TYPE
from djspace.core.models import GenericChoice
from djspace.core.models import UserProfile
from djtools.fields import BINARY_CHOICES
from djtools.fields import GENDER_CHOICES
from djtools.fields import SALUTATION_TITLES
from djtools.fields import STATE_CHOICES
from djtools.fields.localflavor import USPhoneNumberField


RACES = GenericChoice.objects.filter(tags__name__in=['Race']).order_by('name')


class UserForm(forms.Form):
    """Django User data plus salutation and second_name from profile."""

    salutation = forms.CharField(
        widget=forms.Select(choices=SALUTATION_TITLES),
        max_length=16,
        required=False,
    )
    first_name = forms.CharField(max_length=30)
    second_name = forms.CharField(
        label="Second name, middle name or initial",
        max_length=30,
    )
    last_name = forms.CharField(
        max_length=30,
    )


class UserProfileForm(forms.ModelForm):
    """User profile data."""

    registration_type = forms.CharField(
        max_length=32,
        widget=forms.Select(choices=REG_TYPE),
    )
    date_of_birth = forms.DateField(
        label="Date of birth",
        widget=forms.SelectDateWidget(years=BIRTH_YEAR_CHOICES),
    )
    gender = forms.TypedChoiceField(
        choices=GENDER_CHOICES, widget=forms.RadioSelect(),
    )
    race = forms.ModelMultipleChoiceField(
        label="Race and Ethnicity",
        queryset=RACES,
        help_text='Check all that apply',
        widget=forms.CheckboxSelectMultiple(),
    )
    tribe = forms.CharField(
        max_length=128,
        required=False,
    )
    disability = forms.CharField(
        label="Disability status",
        widget=forms.Select(choices=DISABILITY_CHOICES),
    )
    disability_specify = forms.CharField(
        label="Specify if not listed",
        max_length=255,
        required=False,
    )
    us_citizen = forms.TypedChoiceField(
        label="United States Citizen",
        choices=BINARY_CHOICES,
        widget=forms.RadioSelect(),
    )
    military = forms.TypedChoiceField(
        label="Have you served in the United States military?",
        choices=BINARY_CHOICES,
        widget=forms.RadioSelect(),
    )
    address1 = forms.CharField(label="Street address", max_length=128)
    address2 = forms.CharField(label="", max_length=128, required=False)
    city = forms.CharField(max_length=128)
    state = forms.CharField(widget=forms.Select(choices=STATE_CHOICES))
    postal_code = forms.CharField(label="Postal Code", max_length=10)
    address1_current = forms.CharField(
        label="Street address",
        max_length=128,
        required=False,
    )
    address2_current = forms.CharField(label="", max_length=128, required=False)
    city_current = forms.CharField(label="City", max_length=128, required=False)
    state_current = forms.CharField(
        label="State",
        widget=forms.Select(choices=STATE_CHOICES),
        required=False,
    )
    postal_code_current = forms.CharField(
        label="Postal Code",
        max_length=10,
        required=False,
    )
    phone_primary = USPhoneNumberField(
        label="Primary phone",
        widget=forms.TextInput(attrs={'placeholder': 'eg. 123-456-7890'}),
    )
    phone_mobile = USPhoneNumberField(
        label="Cell phone",
        widget=forms.TextInput(attrs={'placeholder': 'eg. 123-456-7890'}),
    )

    class Meta:
        """Information about the form class."""

        model = UserProfile
        exclude = ('user', 'salutation', 'second_name')
        fields = [
            'registration_type',
            'date_of_birth',
            'gender',
            'race',
            'tribe',
            'disability',
            'disability_specify',
            'employment',
            'military',
            'us_citizen',
            'address1_current',
            'address2_current',
            'city_current',
            'state_current',
            'postal_code_current',
            'address1',
            'address2',
            'city',
            'state',
            'postal_code',
            'phone_primary',
            'phone_mobile',
            'media_release',
        ]

    def clean(self):
        """Form validation."""
        cd = super(UserProfileForm, self).clean()
        # current address is required for students
        if cd.get('registration_type') in {'Undergraduate', 'Graduate'}:
            if not cd.get('address1_current'):
                self._errors['address1_current'] = self.error_class(
                    ["Required field"],
                )
            if not cd.get('city_current'):
                self._errors['city_current'] = self.error_class(
                    ["Required field"],
                )
            if not cd.get('state_current'):
                self._errors['state_current'] = self.error_class(
                    ["Required field"],
                )
            if not cd.get('postal_code_current'):
                self._errors['postal_code_current'] = self.error_class(
                    ["Required field"],
                )
        disability_error = (
            cd.get('disability') == 'I have a disability, but it is not listed' and
            cd.get('disability_specify') == ''
        )
        if disability_error:
            self._errors['disability_specify'] = self.error_class(
                ["Please describe your disability"],
            )
        return cd
