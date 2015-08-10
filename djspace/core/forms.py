# -*- coding: utf-8 -*-
from django import forms
from django.contrib import messages
from django.forms.extras.widgets import SelectDateWidget

from djspace.core.models import UserProfile, GenericChoice, BIRTH_YEAR_CHOICES
from djspace.core.models import REG_TYPE, EMPLOYMENT_CHOICES, DISABILITY_CHOICES

from djtools.fields import GENDER_CHOICES, SALUTATION_TITLES, STATE_CHOICES
from djtools.fields import BINARY_CHOICES, YES_NO_DECLINE

from localflavor.us.forms import USPhoneNumberField

RACES = GenericChoice.objects.filter(tags__name__in=["Race"]).order_by("ranking")

import datetime

DOB_YEAR = datetime.date.today().year-10

class SignupForm(forms.Form):
    """
    Gathers auth and user profile data
    """

    registration_type = forms.CharField(
        max_length=32,
        widget=forms.Select(choices=REG_TYPE)
    )
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
    date_of_birth = forms.DateField(
        label = "Date of birth",
        required=False,
        widget=SelectDateWidget(years=range(DOB_YEAR,1929,-1))
    )
    gender = forms.TypedChoiceField(
        choices = GENDER_CHOICES,
        widget = forms.RadioSelect()
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
    disability = forms.CharField(
        label="Disability status",
        widget=forms.Select(choices=DISABILITY_CHOICES)
    )
    disability_specify = forms.CharField(
        label="Specify if not listed",
        max_length=255, required=False
    )
    employment = forms.CharField(
        label="Employment status",
        widget=forms.Select(choices=EMPLOYMENT_CHOICES)
    )
    us_citizen = forms.TypedChoiceField(
        label = "United States Citizen",
        choices = BINARY_CHOICES, widget = forms.RadioSelect()
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
    address1_current = forms.CharField(
        label="Address",
        max_length=128,
        required=False
    )
    address2_current = forms.CharField(
        label="",
        max_length=128,
        required=False
    )
    city_current = forms.CharField(
        max_length=128,
        required=False
    )
    state_current = forms.CharField(
        widget=forms.Select(choices=STATE_CHOICES),
        required=False
    )
    postal_code_current = forms.CharField(
        label="Zip code",
        max_length=10,
        required=False
    )
    phone_primary = USPhoneNumberField(
        label="Primary phone",
        widget=forms.TextInput(attrs={'placeholder': 'eg. 123-456-7890'})
    )
    phone_mobile = USPhoneNumberField(
        label="Cell phone",
        widget=forms.TextInput(attrs={'placeholder': 'eg. 123-456-7890'})
    )
    email_secondary = forms.EmailField(
        label='Secondary e-mail',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Secondary e-mail address'
            }
        )
    )

    def clean(self):
        cd = super(SignupForm, self).clean()
        if not cd.get("date_of_birth"):
            self._errors["date_of_birth"] = self.error_class(
                ["Required field"]
            )
        # current address is required for students
        if (cd.get("registration_type") == "Undergraduate" or \
            cd.get("registration_type") == "Graduate"):
            if not cd.get("address_current_1"):
                self._errors["address_current_1"] = self.error_class(
                    ["Required field"]
                )
            if not cd.get("city_current"):
                self._errors["city_current"] = self.error_class(
                    ["Required field"]
                )
            if not cd.get("state_current"):
                self._errors["state_current"] = self.error_class(
                    ["Required field"]
                )
            if not cd.get("postal_code_current"):
                self._errors["postal_code_current"] = self.error_class(
                    ["Required field"]
                )
        if cd.get("disability") == "I have a disability, but it is not listed"\
          and cd.get("disability_specify") == "":
            self._errors["disability_specify"] = self.error_class(
                ["Please describe your disability"]
            )
        return cd


    def signup(self, request, user):
        cd = self.cleaned_data
        user.first_name = cd['first_name']
        user.last_name = cd['last_name']
        user.save()
        profile = UserProfile(
            user = user,
            updated_by = user,
            salutation = cd['salutation'],
            second_name = cd['second_name'],
            registration_type = cd['registration_type'],
            gender = cd['gender'],
            tribe = cd.get('tribe'),
            disability = cd['disability'],
            employment = cd['employment'],
            us_citizen = cd['us_citizen'],
            date_of_birth = cd['date_of_birth'],
            address_current_1 = cd['address_current_1'],
            address_current_2 = cd.get('address_current_2'),
            address_permanent_1 = cd['address_permanent_1'],
            address_permanent_2 = cd.get('address_permanent_2'),
            city = cd['city'],
            state = cd['state'],
            postal_code = cd['postal_code'],
            phone_primary = cd['phone_primary'],
            phone_mobile = cd['phone_mobile']
        )
        profile.save()
        for r in request.POST.getlist('race'):
            profile.race.add(r)
        profile.save()

        if profile.us_citizen == "No":
            messages.warning(
                request,
                """
                You must be a United States citizen in order to
                apply for grants from NASA.
                """
            )
