# -*- coding: utf-8 -*-
from django import forms
from django.contrib import messages
from django.forms.extras.widgets import SelectDateWidget

from djspace.core.models import BIRTH_YEAR_CHOICES
from djspace.core.models import DISABILITY_CHOICES
from djspace.core.models import EMPLOYMENT_CHOICES
from djspace.core.models import GenericChoice
from djspace.core.models import Photo
from djspace.core.models import REG_TYPE
from djspace.core.models import UserFiles
from djspace.core.models import UserProfile
from djtools.fields import GENDER_CHOICES
from djtools.fields import SALUTATION_TITLES
from djtools.fields import STATE_CHOICES
from djtools.fields import BINARY_CHOICES
from djtools.fields.localflavor import USPhoneNumberField

from allauth.account.models import EmailAddress
from collections import OrderedDict
from datetime import date

DOB_YEAR = date.today().year-10
RACES = GenericChoice.objects.filter(tags__name__in=['Race']).order_by('ranking')


class EmailApplicantsForm(forms.Form):
    """Email form for sending email to applicants."""

    content = forms.CharField(
        required=True, widget=forms.Textarea, label="Email content"
    )
    title = forms.CharField(max_length=50, widget=forms.HiddenInput())
    content_type = forms.CharField(max_length=8, widget=forms.HiddenInput())

    def clean_content(self):
        content = self.cleaned_data['content']

        self._errors['content'] = self.error_class(
            ["Please provide the content of the email"],
        )

        return content


class SignupForm(forms.Form):
    """Gathers auth and user profile data."""

    registration_type = forms.CharField(
        max_length=32,
        widget=forms.Select(choices=REG_TYPE),
    )
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
    last_name = forms.CharField(max_length=30)
    date_of_birth = forms.DateField(
        label = "Date of birth",
        required=False,
        widget=SelectDateWidget(years=range(DOB_YEAR,1929,-1)),
    )
    gender = forms.TypedChoiceField(
        choices = GENDER_CHOICES,
        widget = forms.RadioSelect(),
    )
    race = forms.ModelMultipleChoiceField(
        queryset = RACES,
        help_text = 'Check all that apply',
        widget = forms.CheckboxSelectMultiple(),
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
    employment = forms.CharField(
        label="Employment status",
        widget=forms.Select(choices=EMPLOYMENT_CHOICES),
    )
    military = forms.TypedChoiceField(
        label="Have you served in the United States military?",
        choices=BINARY_CHOICES,
        widget=forms.RadioSelect(),
    )
    us_citizen = forms.TypedChoiceField(
        label="United States Citizen",
        choices=BINARY_CHOICES,
        widget=forms.RadioSelect(),
    )
    address1 = forms.CharField(label="Address", max_length=128)
    address2 = forms.CharField(label="", max_length=128, required=False)
    city = forms.CharField(max_length=128)
    state = forms.CharField(widget=forms.Select(choices=STATE_CHOICES))
    postal_code = forms.CharField(label="Postal Code", max_length=10)
    address1_current = forms.CharField(
        label="Address",
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
    email_secondary = forms.EmailField(
        label='Secondary e-mail',
        widget=forms.TextInput(attrs={'placeholder': 'Secondary e-mail address'}),
    )

    def clean(self):
        """Form validation."""
        cd = super(SignupForm, self).clean()
        # dob is required for this form
        if not cd.get('date_of_birth'):
            self._errors['date_of_birth'] = self.error_class(
                ["Required field"],
            )
        # current address is required for students
        if (cd.get('registration_type') == 'Undergraduate' or \
            cd.get('registration_type') == 'Graduate'):
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
        # check disability and description
        if cd.get('disability') == 'I have a disability, but it is not listed'\
          and cd.get('disability_specify') == '':
            self._errors['disability_specify'] = self.error_class(
                ["Please describe your disability"],
            )

        # check if secondary email already exists in the system
        if cd.get('email_secondary'):
            try:
                EmailAddress.objects.get(email= cd.get('email_secondary'))
                self._errors['email_secondary'] = self.error_class(
                    ["That email already exists in the system"],
                )
                raise forms.ValidationError(
                    """
                        You have submitted an email that already exists
                        in the system. Please provide a different email.
                    """
                )
            except:
                pass

        return cd

    def signup(self, request, user):
        """Required method for the allauth package."""
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
            disability_specify = cd['disability_specify'],
            employment = cd['employment'],
            military = cd['military'],
            us_citizen = cd['us_citizen'],
            date_of_birth = cd['date_of_birth'],
            address1 = cd['address1'],
            address2 = cd.get('address2'),
            city = cd['city'],
            state = cd['state'],
            postal_code = cd['postal_code'],
            address1_current = cd['address1_current'],
            address2_current = cd.get('address2_current'),
            city_current = cd['city_current'],
            state_current = cd['state_current'],
            postal_code_current = cd['postal_code_current'],
            phone_primary = cd['phone_primary'],
            phone_mobile = cd['phone_mobile'],
        )
        profile.save()
        for r in request.POST.getlist('race'):
            profile.race.add(r)
        profile.save()

        if profile.us_citizen == 'No':
            messages.warning(
                request,
                """
                You must be a United States citizen in order to
                apply for grants from NASA.
                """
            )

    class Meta:
        """Information about the form class."""

        fields = [
            'registration_type',
            'salutation',
            'first_name',
            'second_name',
            'last_name',
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
            'email_secondary',
        ]


class PhotoForm(forms.ModelForm):
    """Optional photos."""

    class Meta:
        """Information about the form class."""

        model = Photo
        exclude = ('caption', 'content_type', 'object_id', 'content_object')
        fields = ['phile']


class UserFilesForm(forms.ModelForm):
    """Files required after funding has been approved."""

    def __init__(self, *args, **kwargs):
        """Override of the initialization method to obtain the required list."""
        self.required = kwargs.pop('required', None)
        super(UserFilesForm, self).__init__(*args, **kwargs)

    def clean(self):
        """Form validation."""
        cd = self.cleaned_data
        if self.required:
            for require in self.required:
                if not cd.get(require):
                    self.add_error(require, "Required field")
        return cd

    #def clean_mugshot(self):
        #phile = self.cleaned_data.get('mugshot')
        #if phile.path

    class Meta:
        """Information about the form class."""

        model = UserFiles
        exclude = ('user', 'status')
        fields = ['mugshot', 'biography', 'media_release', 'irs_w9']
