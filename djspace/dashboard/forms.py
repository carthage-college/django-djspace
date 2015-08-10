# -*- coding: utf-8 -*-
from django import forms
from django.forms.extras.widgets import SelectDateWidget

from djspace.core.models import UserProfile, GenericChoice
from djspace.core.models import REG_TYPE, BIRTH_YEAR_CHOICES

from djtools.fields import GENDER_CHOICES, SALUTATION_TITLES, STATE_CHOICES
from djtools.fields import BINARY_CHOICES, YES_NO_DECLINE

from localflavor.us.forms import USPhoneNumberField

RACES = GenericChoice.objects.filter(tags__name__in=["Race"]).order_by("name")

class UserForm(forms.Form):
    """
    Django User data plus salutation and second_name from profile
    """
    salutation = forms.CharField(
        widget=forms.Select(choices=SALUTATION_TITLES),
        max_length=16,
        required=False
    )
    first_name = forms.CharField(
        max_length=30
    )
    second_name = forms.CharField(
        label="Second name, middle name or initial",
        max_length=30
    )
    last_name = forms.CharField(
        max_length=30
    )

class UserProfileForm(forms.ModelForm):
    """
    User profile data
    """

    registration_type = forms.CharField(
        max_length=32,
        widget=forms.Select(choices=REG_TYPE)
    )
    date_of_birth = forms.DateField(
        label = "Date of birth",
        widget=SelectDateWidget(years=BIRTH_YEAR_CHOICES)
    )
    gender = forms.TypedChoiceField(
        choices=GENDER_CHOICES, widget = forms.RadioSelect()
    )
    race = forms.ModelMultipleChoiceField(
        queryset = RACES,
        help_text = 'Check all that apply',
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
        label = "United States Citizen",
        choices=BINARY_CHOICES, widget = forms.RadioSelect()
    )
    address_current_1 = forms.CharField(
        label="Address",
        max_length=128
    )
    address_current_2 = forms.CharField(
        label="",
        max_length=128,
        required=False
    )
    address_permanent_1 = forms.CharField(
        label="Address",
        max_length=128
    )
    address_permanent_2 = forms.CharField(
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
        fields = [
            'registration_type', 'address_current_1','address_current_2',
            'address_permanent_1','address_permanent_2',
            'city','state','postal_code','phone_primary','phone_mobile',
            'date_of_birth','gender','race',
            'tribe','disability','us_citizen'
        ]
