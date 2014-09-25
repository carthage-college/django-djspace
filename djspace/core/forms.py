# -*- coding: utf-8 -*-
from django import forms
from django.contrib import messages
from django.forms.extras.widgets import SelectDateWidget

from djspace.core.models import UserProfile, GenericChoice, BIRTH_YEAR_CHOICES
from djspace.core.models import REG_TYPE

from djtools.fields import GENDER_CHOICES, SALUTATION_TITLES, STATE_CHOICES
from djtools.fields import BINARY_CHOICES, YES_NO_DECLINE

from localflavor.us.forms import USPhoneNumberField

RACES = GenericChoice.objects.filter(tags__name__in=["Race"]).order_by("name")

class SignupForm(forms.Form):
    """
    Gathers auth and user profile data
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
        max_length=30
    )
    last_name = forms.CharField(
        max_length=30
    )
    registration_type = forms.CharField(
        max_length=32,
        widget=forms.Select(choices=REG_TYPE)
    )
    date_of_birth = forms.DateField(
        label = "Date of birth",
        widget=SelectDateWidget(years=range(1996,1929,-1))
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
    disability = forms.TypedChoiceField(
        label="Disability status",
        choices = YES_NO_DECLINE, widget = forms.RadioSelect()
    )
    us_citizen = forms.TypedChoiceField(
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
    phone = USPhoneNumberField(
        widget=forms.TextInput(attrs={'placeholder': 'eg. 123-456-7890'})
    )

    def signup(self, request, user):
        cd = self.cleaned_data
        user.first_name = cd['first_name']
        user.last_name = cd['last_name']
        user.save()
        profile = UserProfile(
            user = user,
            salutation = cd['salutation'],
            second_name = cd['second_name'],
            registration_type = cd['registration_type'],
            gender = cd['gender'],
            tribe = cd.get('tribe'),
            disability = cd['disability'],
            us_citizen = cd['us_citizen'],
            date_of_birth = cd['date_of_birth'],
            address1 = cd['address1'],
            address2 = cd.get('address2'),
            city = cd['city'],
            state = cd['state'],
            postal_code = cd['postal_code'],
            phone = cd['phone']
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
