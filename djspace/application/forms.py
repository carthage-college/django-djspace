# -*- coding: utf-8 -*-
from django import forms
from django.conf import settings
from django.db.models import Count
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from django.core.validators import URLValidator
from django.forms.extras.widgets import SelectDateWidget

from djspace.application.models import *
from djspace.core.models import PAST_FUNDING_YEAR_CHOICES
from djspace.core.utils import get_start_date
from djtools.fields.validators import MimetypeValidator
from djtools.fields import BINARY_CHOICES

from taggit.models import Tag

'''
UploadsForms are for the user dashboard where file uploads
take place after the application has been approved and
additional files are required
'''

class HigherEducationInitiativesForm(forms.ModelForm):

    past_funding = forms.TypedChoiceField(
        label="Have you received WSGC funding within the past five years?",
        choices = BINARY_CHOICES, widget = forms.RadioSelect()
    )
    past_funding_year = forms.CharField(
        label="If 'Yes', what year?",
        widget=forms.Select(choices=PAST_FUNDING_YEAR_CHOICES),
        required = False
    )
    other_fellowship = forms.TypedChoiceField(
        label="""
            Do you currently hold another Federal fellowship or traineeship?
        """,
        choices = BINARY_CHOICES, widget = forms.RadioSelect()
    )

    class Meta:
        model = HigherEducationInitiatives
        exclude = (
            'user','status','funded_code','funds_authorized',
            'authorized_match', 'award_acceptance','final_report',
            'interim_report','invoice','program_match','payment_information'
        )
        fields = (
            'project_title','award_type','funds_requested','proposed_match',
            'source_match','begin_date', 'end_date', 'location','synopsis',
            'proposal','budget','past_funding','past_funding_year',
            'other_fellowship','other_fellowship_explain',
            'finance_officer_name','finance_officer_address',
            'finance_officer_email','finance_officer_phone',
            'grant_officer_name','grant_officer_address',
            'grant_officer_email','grant_officer_phone'
        )


class HigherEducationInitiativesUploadsForm(forms.ModelForm):

    class Meta:
        model = HigherEducationInitiatives
        fields = (
            'award_acceptance','final_report','interim_report',
            'invoice','program_match','payment_information'
        )


class ProfessionalProgramStudentUploadsForm(forms.ModelForm):

    class Meta:
        model = HigherEducationInitiatives
        fields = (
            'award_acceptance','interim_report'
        )


class ResearchInfrastructureForm(forms.ModelForm):

    past_funding = forms.TypedChoiceField(
        label="Have you received WSGC funding within the past five years?",
        choices = BINARY_CHOICES, widget = forms.RadioSelect()
    )
    past_funding_year = forms.CharField(
        label="If 'Yes', what year?",
        widget=forms.Select(choices=PAST_FUNDING_YEAR_CHOICES),
        required = False
    )
    other_fellowship = forms.TypedChoiceField(
        label="""
            Do you currently hold another Federal fellowship or traineeship?
        """,
        choices = BINARY_CHOICES, widget = forms.RadioSelect()
    )

    class Meta:
        model = ResearchInfrastructure
        exclude = (
            'user','status','funded_code','funds_authorized',
            'authorized_match','award_acceptance','final_report',
            'interim_report','payment_information'
        )
        fields = (
            'project_title','award_type','funds_requested','proposed_match',
            'source_match', 'past_funding','past_funding_year',
            'other_fellowship','other_fellowship_explain',
            'begin_date', 'end_date', 'location','synopsis',
            'nasa_mission_directorate',
            'nasa_mission_directorate_other', 'proposal','budget',
            'finance_officer_name','finance_officer_address',
            'finance_officer_email','finance_officer_phone',
            'grant_officer_name','grant_officer_address',
            'grant_officer_email','grant_officer_phone'
        )


class ResearchInfrastructureUploadsForm(forms.ModelForm):

    class Meta:
        model = ResearchInfrastructure
        fields = (
            'award_acceptance','final_report','interim_report',
            'invoice','program_match','payment_information'
        )


class AerospaceOutreachForm(forms.ModelForm):

    project_category = forms.TypedChoiceField(
        choices = PROJECT_CATEGORIES, widget = forms.RadioSelect()
    )
    past_funding = forms.TypedChoiceField(
        label="Have you received WSGC funding within the past five years?",
        choices = BINARY_CHOICES, widget = forms.RadioSelect()
    )
    past_funding_year = forms.CharField(
        label="If 'Yes', what year?",
        widget=forms.Select(choices=PAST_FUNDING_YEAR_CHOICES),
        required = False
    )
    other_funding = forms.TypedChoiceField(
        label="Are you seeking other WSGC funding for this project?",
        choices = BINARY_CHOICES, widget = forms.RadioSelect()
    )
    other_fellowship = forms.TypedChoiceField(
        label="""
            Do you currently hold another Federal fellowship or traineeship?
        """,
        choices = BINARY_CHOICES, widget = forms.RadioSelect()
    )

    class Meta:
        model = AerospaceOutreach
        fields = (
            'project_title','project_category','location','begin_date',
            'end_date', 'funds_requested','proposed_match','source_match',
            'past_funding','past_funding_year',
            'other_funding','other_funding_explain',
            'other_fellowship','other_fellowship_explain',
            'synopsis', 'nasa_mission_directorate',
            'nasa_mission_directorate_other', 'proposal','budget',
            'finance_officer_name','finance_officer_address',
            'finance_officer_email','finance_officer_phone',
            'grant_officer_name','grant_officer_address',
            'grant_officer_email','grant_officer_phone'
        )
        exclude = (
            'user','status','funded_code','funds_authorized',
            'authorized_match','award_acceptance','final_report',
            'interim_report','invoice','program_match','payment_information'
        )


class AerospaceOutreachUploadsForm(forms.ModelForm):

    class Meta:
        model = AerospaceOutreach
        fields = (
            'award_acceptance','final_report','interim_report',
            'invoice','program_match','payment_information'
        )


class SpecialInitiativesForm(forms.ModelForm):

    project_category = forms.TypedChoiceField(
        choices = PROJECT_CATEGORIES, widget = forms.RadioSelect()
    )
    past_funding = forms.TypedChoiceField(
        label="Have you received WSGC funding within the past five years?",
        choices = BINARY_CHOICES, widget = forms.RadioSelect()
    )
    past_funding_year = forms.CharField(
        label="If 'Yes', what year?",
        widget=forms.Select(choices=PAST_FUNDING_YEAR_CHOICES),
        required = False
    )
    other_funding = forms.TypedChoiceField(
        label="Are you seeking other WSGC funding for this project?",
        choices = BINARY_CHOICES, widget = forms.RadioSelect()
    )
    other_fellowship = forms.TypedChoiceField(
        label="""
            Do you currently hold another Federal fellowship or traineeship?
        """,
        choices = BINARY_CHOICES, widget = forms.RadioSelect()
    )
    proposed_match = forms.IntegerField(
        label = "Proposed match (1:1 mimimum)(in $)",
        help_text = """
            Match must be 50% for ongoing program;
            25% for new innovated programs (or)
            programs with significant legacy value.
        """
    )
    source_match = forms.CharField(
        label = "Source(s) of match",
        help_text = """
            Overhead (or indirect costs) cannot exceed 0.5
            of the required matching funds
        """
    )

    class Meta:
        model = SpecialInitiatives
        fields = (
            'project_title','project_category','location','begin_date',
            'end_date', 'funds_requested','proposed_match','source_match',
            'past_funding','past_funding_year',
            'other_funding','other_funding_explain',
            'other_fellowship','other_fellowship_explain',
            'synopsis','nasa_mission_directorate',
            'nasa_mission_directorate_other', 'proposal','budget',
            'finance_officer_name','finance_officer_address',
            'finance_officer_email','finance_officer_phone',
            'grant_officer_name','grant_officer_address',
            'grant_officer_email','grant_officer_phone'
        )
        exclude = (
            'user','status','funded_code','funds_authorized',
            'authorized_match','award_acceptance','final_report',
            'interim_report','invoice','program_match','payment_information'
        )


class SpecialInitiativesUploadsForm(forms.ModelForm):

    class Meta:
        model = SpecialInitiatives
        fields = (
            'award_acceptance','final_report','interim_report',
            'invoice','program_match','payment_information'
        )


class UndergraduateScholarshipForm(forms.ModelForm):

    past_funding = forms.TypedChoiceField(
        label="Have you received WSGC funding within the past five years?",
        choices = BINARY_CHOICES, widget = forms.RadioSelect()
    )
    past_funding_year = forms.CharField(
        label="If 'Yes', what year?",
        widget=forms.Select(choices=PAST_FUNDING_YEAR_CHOICES),
        required = False
    )
    other_funding = forms.TypedChoiceField(
        label="Are you seeking other WSGC funding for this project?",
        choices = BINARY_CHOICES, widget = forms.RadioSelect()
    )
    other_fellowship = forms.TypedChoiceField(
        label="""
            Do you currently hold another Federal fellowship or traineeship?
        """,
        choices = BINARY_CHOICES, widget = forms.RadioSelect()
    )
    academic_institution = forms.TypedChoiceField(
        label = "Application submitted for",
        widget = forms.RadioSelect(),
        choices=ACADEMIC_INSTITUTIONS
    )
    signed_certification = forms.BooleanField(
        label = """
        I certify that I am, will be, or have applied to be a
        full-time undergraduate student at one of the Wisconsin Space
        Grant Consortium colleges or universities during the award period
        covered in this application, and the information
        contained in this application is accurate to the best of my
        knowledge. I understand that, should I receive funding,
        some or all of this scholarship/fellowship may be taxable according
        to IRS regulations and that I am responsible for making sure all
        tax requirements are met.
        """,
        required = True
    )

    class Meta:
        model = UndergraduateScholarship
        exclude = (
            'user','status','funded_code','funds_authorized',
            'authorized_match','award_acceptance','final_report',
            'interim_report'
        )


class UndergraduateScholarshipUploadsForm(forms.ModelForm):

    class Meta:
        model = UndergraduateScholarship
        fields = (
            'award_acceptance','final_report','interim_report'
        )


class StemBridgeScholarshipForm(forms.ModelForm):

    past_funding = forms.TypedChoiceField(
        label="Have you received WSGC funding within the past five years?",
        choices = BINARY_CHOICES, widget = forms.RadioSelect()
    )
    past_funding_year = forms.CharField(
        label="If 'Yes', what year?",
        widget=forms.Select(choices=PAST_FUNDING_YEAR_CHOICES),
        required = False
    )
    other_funding = forms.TypedChoiceField(
        label="Are you seeking other WSGC funding for this project?",
        choices = BINARY_CHOICES, widget = forms.RadioSelect()
    )
    other_fellowship = forms.TypedChoiceField(
        label="""
            Do you currently hold another Federal fellowship or traineeship?
        """,
        choices = BINARY_CHOICES, widget = forms.RadioSelect()
    )
    academic_institution = forms.TypedChoiceField(
        label = "Application submitted for",
        widget = forms.RadioSelect(),
        choices=ACADEMIC_INSTITUTIONS
    )
    signed_certification = forms.BooleanField(
        label = """
        I certify that I am, will be, or have applied to be a
        full-time undergraduate student at one of the Wisconsin Space
        Grant Consortium colleges or universities during the award period
        covered in this application, and the information
        contained in this application is accurate to the best of my
        knowledge. I understand that, should I receive funding,
        some or all of this scholarship/fellowship may be taxable according
        to IRS regulations and that I am responsible for making sure all
        tax requirements are met.
        """,
        required = True
    )

    class Meta:
        model = StemBridgeScholarship
        exclude = (
            'user','status','funded_code','funds_authorized',
            'authorized_match','award_acceptance','final_report',
            'interim_report'
        )


class StemBridgeScholarshipUploadsForm(forms.ModelForm):

    class Meta:
        model = StemBridgeScholarship
        fields = (
            'award_acceptance','final_report','interim_report'
        )


class UndergraduateResearchForm(forms.ModelForm):

    past_funding = forms.TypedChoiceField(
        label="Have you received WSGC funding within the past five years?",
        choices = BINARY_CHOICES, widget = forms.RadioSelect()
    )
    past_funding_year = forms.CharField(
        label="If 'Yes', what year?",
        widget=forms.Select(choices=PAST_FUNDING_YEAR_CHOICES),
        required = False
    )
    other_funding = forms.TypedChoiceField(
        label="Are you seeking other WSGC funding for this project?",
        choices = BINARY_CHOICES, widget = forms.RadioSelect()
    )
    other_fellowship = forms.TypedChoiceField(
        label="""
            Do you currently hold another Federal fellowship or traineeship?
        """,
        choices = BINARY_CHOICES, widget = forms.RadioSelect()
    )
    signed_certification = forms.BooleanField(
        label = """
        I certify that I am, will be, or have applied to be a
        full-time undergraduate student at one of the Wisconsin Space
        Grant Consortium colleges or universities during the award period
        covered in this application, and the information
        contained in this application is accurate to the best of my
        knowledge. I understand that, should I receive funding,
        some or all of this scholarship/fellowship may be taxable according
        to IRS regulations and that I am responsible for making sure all
        tax requirements are met.
        """,
        required = True
    )

    class Meta:
        model = UndergraduateResearch
        exclude = (
            'user','status','funded_code','funds_authorized',
            'authorized_match','award_acceptance','final_report',
            'interim_report'
        )


class UndergraduateResearchUploadsForm(forms.ModelForm):

    class Meta:
        model = UndergraduateResearch
        fields = (
            'award_acceptance','final_report','interim_report',
        )


class GraduateFellowshipForm(forms.ModelForm):

    past_funding = forms.TypedChoiceField(
        label="Have you received WSGC funding within the past five years?",
        choices = BINARY_CHOICES, widget = forms.RadioSelect()
    )
    past_funding_year = forms.CharField(
        label="If 'Yes', what year?",
        widget=forms.Select(choices=PAST_FUNDING_YEAR_CHOICES),
        required = False
    )
    other_fellowship = forms.TypedChoiceField(
        label="""
            Do you currently hold another Federal fellowship or traineeship?
        """,
        choices = BINARY_CHOICES, widget = forms.RadioSelect()
    )
    signed_certification = forms.BooleanField(
        label = """
        I certify that I am, will be, or have applied to be a
        full-time undergraduate student at one of the Wisconsin Space
        Grant Consortium colleges or universities during the award period
        covered in this application, and the information
        contained in this application is accurate to the best of my
        knowledge. I understand that, should I receive funding,
        some or all of this scholarship/fellowship may be taxable according
        to IRS regulations and that I am responsible for making sure all
        tax requirements are met.
        """,
        required = True
    )

    class Meta:
        model = GraduateFellowship
        exclude = (
            'user','status','funded_code','funds_authorized',
            'authorized_match','award_acceptance','final_report',
            'interim_report'
        )


class GraduateFellowshipUploadsForm(forms.ModelForm):

    class Meta:
        model = GraduateFellowship
        fields = (
            'award_acceptance','final_report','interim_report'
        )


class ClarkGraduateFellowshipForm(forms.ModelForm):

    past_funding = forms.TypedChoiceField(
        label="Have you received WSGC funding within the past five years?",
        choices = BINARY_CHOICES, widget = forms.RadioSelect()
    )
    past_funding_year = forms.CharField(
        label="If 'Yes', what year?",
        widget=forms.Select(choices=PAST_FUNDING_YEAR_CHOICES),
        required = False
    )
    other_fellowship = forms.TypedChoiceField(
        label="""
            Do you currently hold another Federal fellowship or traineeship?
        """,
        choices = BINARY_CHOICES, widget = forms.RadioSelect()
    )
    signed_certification = forms.BooleanField(
        label = """
        I certify that I am, will be, or have applied to be a
        full-time undergraduate student at one of the Wisconsin Space
        Grant Consortium colleges or universities during the award period
        covered in this application, and the information
        contained in this application is accurate to the best of my
        knowledge. I understand that, should I receive funding,
        some or all of this scholarship/fellowship may be taxable according
        to IRS regulations and that I am responsible for making sure all
        tax requirements are met.
        """,
        required = True
    )

    class Meta:
        model = ClarkGraduateFellowship
        exclude = (
            'user','status','funded_code','funds_authorized',
            'authorized_match','award_acceptance','final_report',
            'interim_report'
        )


class ClarkGraduateFellowshipUploadsForm(forms.ModelForm):

    class Meta:
        model = ClarkGraduateFellowship
        fields = (
            'award_acceptance','final_report','interim_report'
        )


class HighAltitudeBalloonPayloadForm(forms.ModelForm):

    commit = forms.TypedChoiceField(
        label="""
            Will you be able to commit 32-40 hours/week
            to this 10 week summer experience?
        """,
        required = True,
        choices = BINARY_CHOICES, widget = forms.RadioSelect()
    )
    past_funding = forms.TypedChoiceField(
        label="Have you received WSGC funding within the past five years?",
        choices = BINARY_CHOICES, widget = forms.RadioSelect()
    )
    past_funding_year = forms.CharField(
        label="If 'Yes', what year?",
        widget=forms.Select(choices=PAST_FUNDING_YEAR_CHOICES),
        required = False
    )
    other_fellowship = forms.TypedChoiceField(
        label="""
            Do you currently hold another Federal fellowship or traineeship?
        """,
        choices = BINARY_CHOICES, widget = forms.RadioSelect()
    )

    class Meta:
        model = HighAltitudeBalloonPayload
        exclude = (
            'user','status','funded_code','funds_authorized',
            'authorized_match','award_acceptance','final_report',
            'interim_report'
        )


class HighAltitudeBalloonPayloadUploadsForm(forms.ModelForm):

    class Meta:
        model = HighAltitudeBalloonPayload
        fields = (
            'award_acceptance','final_report','interim_report'
        )


class HighAltitudeBalloonLaunchForm(forms.ModelForm):

    past_funding = forms.TypedChoiceField(
        label="Have you received WSGC funding within the past five years?",
        choices = BINARY_CHOICES, widget = forms.RadioSelect()
    )
    past_funding_year = forms.CharField(
        label="If 'Yes', what year?",
        widget=forms.Select(choices=PAST_FUNDING_YEAR_CHOICES),
        required = False
    )
    other_fellowship = forms.TypedChoiceField(
        label="""
            Do you currently hold another Federal fellowship or traineeship?
        """,
        choices = BINARY_CHOICES, widget = forms.RadioSelect()
    )

    class Meta:
        model = HighAltitudeBalloonLaunch
        exclude = (
            'user','status','commit','funded_code','funds_authorized',
            'authorized_match','award_acceptance','final_report',
            'interim_report'
        )


class HighAltitudeBalloonLaunchUploadsForm(forms.ModelForm):

    class Meta:
        model = HighAltitudeBalloonLaunch
        fields = (
            'award_acceptance','final_report','interim_report'
        )


class RocketLaunchTeamForm(forms.ModelForm):
    '''
    Form that handles the create/update for Rocket Launch Teams
    '''
    co_advisor = forms.CharField(
        label = "Co-Advisor",
        required = False,
        help_text = '''
            Enter the last name or first name of the Co-Advisor to see results
            from which to choose.
        ''',
    )
    leader = forms.CharField(
        label = "Team Lead",
        required = True,
        help_text = '''
            Enter the last name or first name of the team leader to see results
            from which to choose.
        ''',
    )
    past_funding = forms.TypedChoiceField(
        label="Have you received WSGC funding within the past five years?",
        choices = BINARY_CHOICES, widget = forms.RadioSelect()
    )
    past_funding_year = forms.CharField(
        label="If 'Yes', what year?",
        widget=forms.Select(choices=PAST_FUNDING_YEAR_CHOICES),
        required = False
    )
    other_fellowship = forms.TypedChoiceField(
        label="""
            Do you currently hold another Federal fellowship or traineeship?
        """,
        choices = BINARY_CHOICES, widget = forms.RadioSelect()
    )

    class Meta:
        model = RocketLaunchTeam
        exclude = (
            'user','status','funded_code','funds_authorized',
            'authorized_match','members','award_acceptance',
            'interim_progress_report','interim_report',
            'preliminary_design_report','final_design_report','final_report',
            'team_roster','flight_demo','final_motor_selection','lodging_list',
            'critical_design_report','oral_presentation','proceeding_paper',
            'flight_readiness_report','post_flight_performance_report',
            'education_outreach','verified_budget','payment_information_form',
            'invoice','charges_certification','institutional_w9'
        )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(RocketLaunchTeamForm, self).__init__(*args, **kwargs)

    def clean_co_advisor(self):
        '''
        Assign a User object to co-advisor
        '''

        cd = self.cleaned_data
        cid = cd.get('co_advisor')

        if cid:
            try:
                user = User.objects.get(pk=cid)
                cd['co_advisor'] = user
                self.request.session['co_advisor_name'] = u'{}, {}'.format(
                    user.last_name, user.first_name
                )
            except:
                self._errors["co_advisor"] = self.error_class(
                    ["That User does not exist in the system"]
                )
        else:
            cd['co_advisor'] = None

        return cd['co_advisor']

    def clean_leader(self):
        '''
        Assign a User object to co-advisor
        '''

        cd = self.cleaned_data
        lid = cd.get('leader')

        if lid:
            try:
                user = User.objects.get(pk=lid)
                cd['leader'] = user
                self.request.session['leader_name'] = u'{}, {}'.format(
                    user.last_name, user.first_name
                )
            except:
                self._errors["leader"] = self.error_class(
                    ["That User does not exist in the system"]
                )
        else:
            self._errors["leader"] = self.error_class(
                ["Required field"]
            )

        return cd['leader']


class RocketLaunchTeamUploadsForm(forms.ModelForm):

    class Meta:
        model = RocketLaunchTeam
        fields = (
            'award_acceptance','interim_progress_report',
            'preliminary_design_report','final_design_report','team_roster',
            'budget','flight_demo','final_motor_selection','lodging_list',
            'critical_design_report','oral_presentation',
            'post_flight_performance_report','education_outreach',
            'flight_readiness_report','proceeding_paper',
            'verified_budget','payment_information_form',
            'invoice','charges_certification','institutional_w9'
        )


class FirstNationsRocketCompetitionForm(forms.ModelForm):

    past_funding = forms.TypedChoiceField(
        label="Have you received WSGC funding within the past five years?",
        choices = BINARY_CHOICES, widget = forms.RadioSelect()
    )
    past_funding_year = forms.CharField(
        label="If 'Yes', what year?",
        widget=forms.Select(choices=PAST_FUNDING_YEAR_CHOICES),
        required = False
    )
    media_release = forms.FileField(
        validators=[MimetypeValidator('application/pdf')],
        max_length=768,
        help_text="PDF format"
    )

    class Meta:
        model = FirstNationsRocketCompetition
        exclude = (
            'user','status','funded_code','funds_authorized',
            'authorized_match','award_acceptance','interim_report',
            'final_report'
        )


    def __init__(self, *args, **kwargs):
        super(FirstNationsRocketCompetitionForm, self).__init__(
            *args,**kwargs
        )
        self.fields['team'].queryset = RocketLaunchTeam.objects.filter(
            competition__contains="First Nations"
        ).filter(date_created__gte=get_start_date()).order_by("name")
        instance = kwargs.get('instance', None)
        if instance:
            self.fields['media_release'].initial = instance.get_media_release()

class FirstNationsRocketCompetitionUploadsForm(forms.ModelForm):
    """
    WSGC have removed the requirement for Award Acceptance letter but
    we will keep this form class in place for when they decide to go
    back to requiring it.
    """

    class Meta:
        model = FirstNationsRocketCompetition
        fields = (
            'award_acceptance',
        )


class MidwestHighPoweredRocketCompetitionForm(forms.ModelForm):

    past_funding = forms.TypedChoiceField(
        label="Have you received WSGC funding within the past five years?",
        choices = BINARY_CHOICES, widget = forms.RadioSelect()
    )
    past_funding_year = forms.CharField(
        label="If 'Yes', what year?",
        widget=forms.Select(choices=PAST_FUNDING_YEAR_CHOICES),
        required = False
    )
    other_fellowship = forms.TypedChoiceField(
        label="""
            Do you currently hold another Federal fellowship or traineeship?
        """,
        choices = BINARY_CHOICES, widget = forms.RadioSelect()
    )
    past_participation = forms.TypedChoiceField(
        label="Have you previously participated in Collegiate Rocket Launch?",
        choices = BINARY_CHOICES, widget = forms.RadioSelect()
    )

    class Meta:
        model = MidwestHighPoweredRocketCompetition
        exclude = (
            'user','status','funded_code','funds_authorized',
            'authorized_match','award_acceptance','interim_report',
            'final_report'
        )

    def __init__(self, *args, **kwargs):
        super(MidwestHighPoweredRocketCompetitionForm, self).__init__(
            *args,**kwargs
        )
        self.fields['team'].queryset = RocketLaunchTeam.objects.annotate(
            count=Count('members')
        ).filter(
            competition__in=["Midwest High Powered Rocket Competition"]
        ).filter(
            date_created__gte=get_start_date()
        ).exclude(
            count__gte=settings.ROCKET_LAUNCH_COMPETITION_TEAM_LIMIT
        ).order_by("name")


class MidwestHighPoweredRocketCompetitionUploadsForm(forms.ModelForm):

    class Meta:
        model = MidwestHighPoweredRocketCompetition
        fields = (
            'award_acceptance',
        )


class CollegiateRocketCompetitionForm(forms.ModelForm):

    past_funding = forms.TypedChoiceField(
        label="Have you received WSGC funding within the past five years?",
        choices = BINARY_CHOICES, widget = forms.RadioSelect()
    )
    past_funding_year = forms.CharField(
        label="If 'Yes', what year?",
        widget=forms.Select(choices=PAST_FUNDING_YEAR_CHOICES),
        required = False
    )
    other_fellowship = forms.TypedChoiceField(
        label="""
            Do you currently hold another Federal fellowship or traineeship?
        """,
        choices = BINARY_CHOICES, widget = forms.RadioSelect()
    )

    class Meta:
        model = CollegiateRocketCompetition
        exclude = (
            'user','status','funded_code','funds_authorized',
            'authorized_match','award_acceptance','interim_report',
            'final_report'
        )


    def __init__(self, *args, **kwargs):
        super(CollegiateRocketCompetitionForm, self).__init__(
            *args,**kwargs
        )
        self.fields['team'].queryset = RocketLaunchTeam.objects.annotate(
            count=Count('members')
        ).filter(competition__in=["Collegiate Rocket Competition"]).filter(
            date_created__gte=get_start_date()
        ).exclude(count__gte=settings.ROCKET_LAUNCH_COMPETITION_TEAM_LIMIT).order_by("name")


class CollegiateRocketCompetitionUploadsForm(forms.ModelForm):

    class Meta:
        model = CollegiateRocketCompetition
        fields = (
            'award_acceptance',
        )


class NasaCompetitionForm(forms.ModelForm):

    past_funding = forms.TypedChoiceField(
        label="Have you received WSGC funding within the past five years?",
        choices = BINARY_CHOICES, widget = forms.RadioSelect()
    )
    past_funding_year = forms.CharField(
        label="If 'Yes', what year?",
        widget=forms.Select(choices=PAST_FUNDING_YEAR_CHOICES),
        required = False
    )
    other_fellowship = forms.TypedChoiceField(
        label="""
            Do you currently hold another Federal fellowship or traineeship?
        """,
        choices = BINARY_CHOICES, widget = forms.RadioSelect()
    )
    program_acceptance = forms.TypedChoiceField(
        label = "Has your team applied and been accepted into the program?",
        choices = BINARY_CHOICES, widget = forms.RadioSelect()
    )

    class Meta:
        model = NasaCompetition
        exclude = (
            'user','status','funded_code','funds_authorized',
            'authorized_match','award_acceptance','final_report',
            'interim_report','invoice','program_match','payment_information'
        )


    def clean(self):
        """
        Check "other" fields if need be
        """
        cd = self.cleaned_data

        if cd.get("competition_type") == "Other":
            if cd.get("competition_type_other") == "":
                self._errors["competition_type_other"] = self.error_class(
                    ["Required field"]
                )

        if cd.get("facility_name") == "Other":
            if cd.get("facility_name_other") == "":
                self._errors["facility_name_other"] = self.error_class(
                    ["Required field"]
                )

        return cd


class NasaCompetitionUploadsForm(forms.ModelForm):

    class Meta:
        model = NasaCompetition
        fields = (
            'award_acceptance','final_report','interim_report','invoice',
            'program_match','payment_information'
        )


class IndustryInternshipForm(forms.ModelForm):

    past_funding = forms.TypedChoiceField(
        label="Have you received WSGC funding within the past five years?",
        choices = BINARY_CHOICES, widget = forms.RadioSelect()
    )
    past_funding_year = forms.CharField(
        label="If 'Yes', what year?",
        widget=forms.Select(choices=PAST_FUNDING_YEAR_CHOICES),
        required = False
    )
    other_fellowship = forms.TypedChoiceField(
        label="""
            Do you currently hold another Federal fellowship or traineeship?
        """,
        choices = BINARY_CHOICES, widget = forms.RadioSelect()
    )

    class Meta:
        model = IndustryInternship
        exclude = (
            'user','status','funded_code','work_plan','funds_authorized',
            'authorized_match','award_acceptance','final_report',
            'interim_report','invoice','program_match','payment_information'
        )


class IndustryInternshipUploadsForm(forms.ModelForm):

    class Meta:
        model = IndustryInternship
        fields = (
            'budget','award_acceptance','final_report','interim_report',
            'invoice','program_match','payment_information'
        )


class ProfessionalProgramStudentForm(forms.ModelForm):

    past_funding = forms.TypedChoiceField(
        label="Have you received WSGC funding within the past five years?",
        choices = BINARY_CHOICES, widget = forms.RadioSelect()
    )
    past_funding_year = forms.CharField(
        label="If 'Yes', what year?",
        widget=forms.Select(choices=PAST_FUNDING_YEAR_CHOICES),
        required = False
    )
    mentor = forms.CharField(
        label = "Mentor",
        required = True,
        help_text = '''
            Enter the last name or first name of mentor to see results
            from which to choose.
        ''',
    )

    class Meta:
        model = ProfessionalProgramStudent
        fields = (
            'program','mentor','award_acceptance','budget'
        )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(ProfessionalProgramStudentForm, self).__init__(*args, **kwargs)

    def clean_mentor(self):
        '''
        Assign a User object to co-advisor
        '''

        cd = self.cleaned_data
        mid = cd.get('mentor')

        if mid:
            #try:
            if True:
                user = User.objects.get(pk=mid)
                cd['mentor'] = user
                self.request.session['mentor_name'] = u'{}, {}'.format(
                    user.last_name, user.first_name
                )
            #except:
                #self._errors["mentor"] = self.error_class(
                    #["That User does not exist in the system"]
                #)
        else:
            self._errors["mentor"] = self.error_class(
                ["Required field"]
            )

        return cd['mentor']

