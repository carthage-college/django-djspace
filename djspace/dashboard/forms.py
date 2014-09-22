# -*- coding: utf-8 -*-
from django import forms

from djspace.registration.choices import RACES
from djspace.core.models import UserProfile

from djtools.fields import GENDER_CHOICES, SALUTATION_TITLES, STATE_CHOICES
from djtools.fields import BINARY_CHOICES, YES_NO_DECLINE

from localflavor.us.forms import USPhoneNumberField

class UserProfileForm(forms.ModelForm):
    """
    User profile data
    """

    date_of_birth = forms.DateField(
        label = "Date of birth",
        widget=forms.TextInput(attrs={'placeholder': 'Format: mm/dd/yyyy'})
    )
    gender = forms.TypedChoiceField(
        choices=GENDER_CHOICES, widget = forms.RadioSelect()
    )
    race = forms.MultipleChoiceField(
        help_text = 'Check all that apply',
        choices=RACES,
        widget = forms.CheckboxSelectMultiple()
    )
    tribe = forms.CharField(
        max_length=128,
        required=False
    )
    disability = forms.TypedChoiceField(
        label="Disability status",
        choices=YES_NO_DECLINE, widget = forms.RadioSelect()
    )
    us_citizen = forms.TypedChoiceField(
        choices=BINARY_CHOICES, widget = forms.RadioSelect()
    )
    address1 = forms.CharField(
        label="Address",
        max_length=128
    )
    address2 = forms.CharField(
        label="",
        max_length=128,
        required=False
    )
    city = forms.CharField(
        max_length=128
    )
    state = forms.CharField(
        widget=forms.Select(choices=STATE_CHOICES)
    )
    postal_code = forms.CharField(
        label="Zip code",
        max_length=10
    )
    phone = USPhoneNumberField(
        widget=forms.TextInput(attrs={'placeholder': 'eg. 123-456-7890'})
    )

    class Meta:
        model = UserProfile
        exclude = ('user','salutation','second_name')

