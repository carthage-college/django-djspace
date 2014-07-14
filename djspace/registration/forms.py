# -*- coding: utf-8 -*-

from django import forms

from djspace.registration.models import MyModel

class MyForm(forms.ModelForm):

    class Meta:
        model = MyModel

