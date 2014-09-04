# -*- coding: utf-8 -*-

from django import forms

from djspace.registration.models.undergraduate import Undergraduate
from djspace.registration.models.graduate import Graduate
from djspace.registration.models.professional import Professional
from djspace.registration.models.professor import Professor
from djspace.registration.models.k12educator import K12educator

class UndergraduateForm(forms.ModelForm):
    """
    A form to collect undergraduate information
    """
    
    citizen = forms.ChoiceField(
        choices=BINARY_CHOICES,
        widget=forms.RadioSelect()
    )
    
    def __init__(self, *args, **kwargs):
        super(UndergraduateForm, self).__init__(*args, **kwargs)
        self.fields.pop('salutation')
        self.fields.pop('maiden')
        self.fields.pop('additional')
        self.fields.pop('title_department')
        self.fields.pop('webpage')
        self.fields.pop('wsgc_advisor_salutation')
        self.fields.pop('wsgc_advisor_first')
        self.fields.pop('wsgc_advisor_middle')
        self.fields.pop('wsgc_advisor_last')
        self.fields.pop('wsgc_advisor_title_department')
        self.fields.pop('wsgc_advisor_email')
        self.fields.pop('wsgc_advisor_confirm_email')
        self.fields.pop('wsgc_advisor_phone')
        self.fields.pop('highschool_street')
        self.fields.pop('highschool_city')
        self.fields.pop('highschool_state')
        self.fields.pop('highschool_zip')
        
    class Meta:
        model = Undergraduate


class GraduateForm(forms.ModelForm):
    """
    A form to collect graduate information
    """
    
    citizen = forms.ChoiceField(
        choices=BINARY_CHOICES,
        widget=forms.RadioSelect()
    )

    class Meta:
        model = Graduate


class ProfessionalForm(forms.ModelForm):
    """
    A form to collect professional information
    """
    
    citizen = forms.ChoiceField(
        choices=BINARY_CHOICES,
        widget=forms.RadioSelect()
    )

    def __init__(self, *args, **kwargs):
        super(ProfessionalForm, self).__init__(*args, **kwargs)
        self.fields.pop('salutation')
        self.fields.pop('maiden')
        self.fields.pop('additional')
        self.fields.pop('title_department')
        self.fields.pop('webpage')
        self.fields.pop('secondary')
        self.fields.pop('secondary_other')
        self.fields.pop('tribe')

    class Meta:
        model = Professional


class ProfessorForm(forms.ModelForm):
    """
    A form to collect professor information
    """
    
    citizen = forms.ChoiceField(
        choices=BINARY_CHOICES,
        widget=forms.RadioSelect()
    )

    class Meta:
        model = Professor


class K12educatorForm(forms.ModelForm):
    """
    A form to collect K12 information
    """
    
    citizen = forms.ChoiceField(
        choices=BINARY_CHOICES,
        widget=forms.RadioSelect()
    )

    def __init__(self, *args, **kwargs):
        super(K12educatorForm, self).__init__(*args, **kwargs)
        self.fields.pop('salutation')
        self.fields.pop('title_department')
        self.fields.pop('webpage')
        self.fields.pop('secondary')
        self.fields.pop('secondary_other')

    class Meta:
        model = K12educator
