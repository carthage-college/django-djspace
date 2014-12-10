# -*- coding: utf-8 -*-

from django import forms

from djspace.application.models import *

class HigherEducationInitiativesForm(forms.ModelForm):

    class Meta:
        model = HigherEducationInitiatives
        exclude = ('user','status','funds_authorized')


class ResearchInfrastructureForm(forms.ModelForm):

    class Meta:
        model = ResearchInfrastructure
        exclude = ('user','status','funds_authorized')


class AerospaceOutreachForm(forms.ModelForm):

    class Meta:
        model = AerospaceOutreach
        exclude = ('user','status','funds_authorized')


class SpecialInitiativesForm(forms.ModelForm):

    proposed_match = forms.IntegerField(
        label = "Proposed match (1:1 mimimum)(in $)",
        help_text = """
            Match must be 50% for ongoing program;
            25% for new innovated programs (or)
            programs with significant legacy value.
        """
    )
    source_match = forms.IntegerField(
        label = "Source(s) of match",
        help_text = """
            Overhead (or indirect costs) cannot exceed 0.5
            of the required matching funds
        """
    )

    class Meta:
        model = SpecialInitiatives
        exclude = ('user','status','funds_authorized')


class UndergraduateScholarshipForm(forms.ModelForm):

    class Meta:
        model = UndergraduateScholarship
        exclude = ('user','status')


class UndergraduateResearchForm(forms.ModelForm):

    class Meta:
        model = UndergraduateResearch
        exclude = ('user','status','funds_authorized')


class GraduateFellowshipForm(forms.ModelForm):

    class Meta:
        model = GraduateFellowship
        exclude = ('user','status','funds_authorized')


class ClarkGraduateFellowshipForm(forms.ModelForm):

    class Meta:
        model = ClarkGraduateFellowship
        exclude = ('user','status','funds_authorized')

class HighAltitudeBalloonPayloadForm(forms.ModelForm):

    class Meta:
        model = HighAltitudeBalloonPayload
        exclude = ('user','status')

class HighAltitudeBalloonLaunchForm(forms.ModelForm):

    class Meta:
        model = HighAltitudeBalloonLaunch
        exclude = ('user','status')

class FirstNationsLaunchCompetitionForm(forms.ModelForm):

    class Meta:
        model = FirstNationsLaunchCompetition
        exclude = ('user','status')

