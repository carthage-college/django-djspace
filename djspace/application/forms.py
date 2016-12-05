# -*- coding: utf-8 -*-
from django import forms
from django.conf import settings
from django.db.models import Count
from django.contrib.auth.models import User
from django.forms.extras.widgets import SelectDateWidget

from djspace.core.utils import get_start_date
from djspace.application.models import *
from djtools.fields.validators import MimetypeValidator
from djtools.fields import BINARY_CHOICES

from taggit.models import Tag


class HigherEducationInitiativesForm(forms.ModelForm):

    other_fellowship = forms.TypedChoiceField(
        label="""
            Do you currently hold another Federal fellowship or traineeship?
        """,
        choices = BINARY_CHOICES, widget = forms.RadioSelect()
    )

    class Meta:
        model = HigherEducationInitiatives
        exclude = (
            'user','status','funds_authorized','authorized_match',
            'award_acceptance','final_report','interim_report',
            'invoice','program_match','payment_information'
        )

        fields = [
            'project_title','award_type','funds_requested','proposed_match',
            'source_match','begin_date', 'end_date', 'location','synopsis',
            'proposal','other_fellowship','other_fellowship_explain',
            'finance_officer_name','finance_officer_address',
            'finance_officer_email','finance_officer_phone',
            'grant_officer_name','grant_officer_address',
            'grant_officer_email','grant_officer_phone'
        ]


class HigherEducationInitiativesUploadsForm(forms.ModelForm):

    class Meta:
        model = HigherEducationInitiatives
        fields = (
            'award_acceptance','final_report','interim_report',
            'invoice','program_match','payment_information'
        )


class ResearchInfrastructureForm(forms.ModelForm):

    other_fellowship = forms.TypedChoiceField(
        label="""
            Do you currently hold another Federal fellowship or traineeship?
        """,
        choices = BINARY_CHOICES, widget = forms.RadioSelect()
    )

    class Meta:
        model = ResearchInfrastructure
        exclude = (
            'user','status','funds_authorized','authorized_match',
            'award_acceptance','final_report','interim_report',
            'payment_information'
        )
        fields = [
            'project_title','award_type','funds_requested','proposed_match',
            'source_match',
            'other_fellowship','other_fellowship_explain',
            'begin_date', 'end_date', 'location','synopsis',
            'nasa_mission_directorate',
            'nasa_mission_directorate_other', 'proposal',
            'finance_officer_name','finance_officer_address',
            'finance_officer_email','finance_officer_phone',
            'grant_officer_name','grant_officer_address',
            'grant_officer_email','grant_officer_phone'
        ]


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
        fields = [
            'project_title','project_category','location','begin_date',
            'end_date', 'funds_requested','proposed_match','source_match',
            'other_funding','other_funding_explain',
            'other_fellowship','other_fellowship_explain',
            'synopsis', 'nasa_mission_directorate',
            'nasa_mission_directorate_other', 'proposal',
            'finance_officer_name','finance_officer_address',
            'finance_officer_email','finance_officer_phone',
            'grant_officer_name','grant_officer_address',
            'grant_officer_email','grant_officer_phone'
        ]
        exclude = (
            'user','status','funds_authorized','authorized_match',
            'award_acceptance','final_report','interim_report',
            'invoice','program_match','payment_information'
        )


class AerospaceOutreachUploadsForm(forms.ModelForm):

    other_fellowship = forms.TypedChoiceField(
        label="""
            Do you currently hold another Federal fellowship or traineeship?
        """,
        choices = BINARY_CHOICES, widget = forms.RadioSelect()
    )

    class Meta:
        model = AerospaceOutreach
        fields = (
            'award_acceptance','final_report','interim_report',
            'other_fellowship','other_fellowship_explain',
            'invoice','program_match','payment_information'
        )


class SpecialInitiativesForm(forms.ModelForm):

    project_category = forms.TypedChoiceField(
        choices = PROJECT_CATEGORIES, widget = forms.RadioSelect()
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
        fields = [
            'project_title','project_category','location','begin_date',
            'end_date', 'funds_requested','proposed_match','source_match',
            'other_funding','other_funding_explain',
            'other_fellowship','other_fellowship_explain',
            'synopsis','nasa_mission_directorate',
            'nasa_mission_directorate_other', 'proposal',
            'finance_officer_name','finance_officer_address',
            'finance_officer_email','finance_officer_phone',
            'grant_officer_name','grant_officer_address',
            'grant_officer_email','grant_officer_phone'
        ]
        exclude = (
            'user','status','funds_authorized','authorized_match',
            'award_acceptance','final_report','interim_report',
            'invoice','program_match','payment_information'
        )


class SpecialInitiativesUploadsForm(forms.ModelForm):

    class Meta:
        model = SpecialInitiatives
        fields = (
            'award_acceptance','final_report','interim_report',
            'other_fellowship','other_fellowship_explain',
            'invoice','program_match','payment_information'
        )


class UndergraduateScholarshipForm(forms.ModelForm):

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

    class Meta:
        model = UndergraduateScholarship
        exclude = (
            'user','status','funds_authorized','authorized_match',
            'other_fellowship','other_fellowship_explain',
            'award_acceptance','final_report','interim_report'
        )


class UndergraduateScholarshipUploadsForm(forms.ModelForm):

    class Meta:
        model = UndergraduateScholarship
        fields = (
            'award_acceptance','final_report','interim_report'
        )


class StemBridgeScholarshipForm(forms.ModelForm):

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
    signed_certification = forms.FileField(
        help_text=mark_safe('''
            Before beginning the application process,
            please print, obtain signatures, and scan the<br>
            <a href="/live/files/2911-ugp17certification-form-pdf" target="_blank">
            signed certification document
            </a>
        ''')
    )
    academic_institution = forms.TypedChoiceField(
        label = "Application submitted for",
        widget = forms.RadioSelect(),
        choices=ACADEMIC_INSTITUTIONS
    )

    class Meta:
        model = StemBridgeScholarship
        exclude = (
            'user','status','funds_authorized','authorized_match',
            'other_fellowship','other_fellowship_explain',
            'award_acceptance','final_report','interim_report'
        )


class StemBridgeScholarshipUploadsForm(forms.ModelForm):

    class Meta:
        model = StemBridgeScholarship
        fields = (
            'award_acceptance','final_report','interim_report'
        )


class UndergraduateResearchForm(forms.ModelForm):

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
        model = UndergraduateResearch
        exclude = (
            'user','status','funds_authorized','authorized_match',
            'other_fellowship','other_fellowship_explain',
            'award_acceptance','final_report','interim_report'
        )


class UndergraduateResearchUploadsForm(forms.ModelForm):

    class Meta:
        model = UndergraduateResearch
        fields = (
            'award_acceptance','final_report','interim_report',
        )


class GraduateFellowshipForm(forms.ModelForm):

    other_fellowship = forms.TypedChoiceField(
        label="""
            Do you currently hold another Federal fellowship or traineeship?
        """,
        choices = BINARY_CHOICES, widget = forms.RadioSelect()
    )

    class Meta:
        model = GraduateFellowship
        exclude = (
            'user','status','funds_authorized','authorized_match',
            'other_fellowship','other_fellowship_explain',
            'award_acceptance','final_report','interim_report'
        )


class GraduateFellowshipUploadsForm(forms.ModelForm):

    class Meta:
        model = GraduateFellowship
        fields = (
            'award_acceptance','final_report','interim_report'
        )


class ClarkGraduateFellowshipForm(forms.ModelForm):

    other_fellowship = forms.TypedChoiceField(
        label="""
            Do you currently hold another Federal fellowship or traineeship?
        """,
        choices = BINARY_CHOICES, widget = forms.RadioSelect()
    )

    class Meta:
        model = ClarkGraduateFellowship
        exclude = (
            'user','status','funds_authorized','authorized_match',
            'other_fellowship','other_fellowship_explain',
            'award_acceptance','final_report','interim_report'
        )


class ClarkGraduateFellowshipUploadsForm(forms.ModelForm):

    class Meta:
        model = ClarkGraduateFellowship
        fields = (
            'award_acceptance','final_report','interim_report'
        )


class HighAltitudeBalloonPayloadForm(forms.ModelForm):

    other_fellowship = forms.TypedChoiceField(
        label="""
            Do you currently hold another Federal fellowship or traineeship?
        """,
        choices = BINARY_CHOICES, widget = forms.RadioSelect()
    )

    class Meta:
        model = HighAltitudeBalloonPayload
        exclude = (
            'user','status','funds_authorized','authorized_match',
            'other_fellowship','other_fellowship_explain',
            'award_acceptance','final_report','interim_report'
        )


class HighAltitudeBalloonPayloadUploadsForm(forms.ModelForm):

    class Meta:
        model = HighAltitudeBalloonPayload
        fields = (
            'award_acceptance','final_report','interim_report'
        )


class HighAltitudeBalloonLaunchForm(forms.ModelForm):

    other_fellowship = forms.TypedChoiceField(
        label="""
            Do you currently hold another Federal fellowship or traineeship?
        """,
        choices = BINARY_CHOICES, widget = forms.RadioSelect()
    )

    class Meta:
        model = HighAltitudeBalloonLaunch
        exclude = (
            'user','status','funds_authorized','authorized_match',
            'other_fellowship','other_fellowship_explain',
            'award_acceptance','final_report','interim_report'
        )


class HighAltitudeBalloonLaunchUploadsForm(forms.ModelForm):

    class Meta:
        model = HighAltitudeBalloonLaunch
        fields = (
            'award_acceptance','final_report','interim_report'
        )


class RocketLaunchTeamForm(forms.ModelForm):
    """
    Form that handles the create/update for Rocket Launch Teams
    """

    leader = forms.CharField(
        label = "Team Lead",
        help_text = '''
            Enter the last name or first name of the team leader to see results
            from which to choose.
        ''',
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
            'user','status','funds_authorized','authorized_match','members',
            'award_acceptance','interim_progress_report','interim_report',
            'preliminary_design_report','final_design_report','final_report',
            'team_roster','flight_demo','final_motor_selection','lodging_list',
            'critical_design_report','oral_presentation','proceeding_paper',
            'flight_readiness_report','post_flight_performance_report',
            'education_outreach'
        )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(RocketLaunchTeamForm, self).__init__(*args, **kwargs)

    def clean(self):
        """
        Assign a User object to leader
        """
        cd = self.cleaned_data
        lid = cd.get("leader")
        if lid:
            try:
                user = User.objects.get(pk=lid)
                cd["leader"] = user
                self.request.session["leader_id"] = user.id
                self.request.session["leader_name"] = u"{}, {}".format(
                    user.last_name, user.first_name
                )
            except:
                cd["leader"] = None
        else:
            cd["leader"] = None

        return cd


class RocketLaunchTeamUploadsForm(forms.ModelForm):

    class Meta:
        model = RocketLaunchTeam
        fields = (
            'award_acceptance','interim_progress_report',
            'preliminary_design_report','final_design_report','team_roster',
            'budget','flight_demo','final_motor_selection','lodging_list',
            'critical_design_report','oral_presentation',
            'post_flight_performance_report','education_outreach',
            'flight_readiness_report','proceeding_paper'
        )


class FirstNationsRocketCompetitionForm(forms.ModelForm):
    media_release = forms.FileField(
        validators=[MimetypeValidator('application/pdf')],
        max_length=768,
        help_text="PDF format"
    )

    class Meta:
        model = FirstNationsRocketCompetition
        exclude = (
            'user','status','funds_authorized','authorized_match',
            'award_acceptance','interim_report','final_report'
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

    other_fellowship = forms.TypedChoiceField(
        label="""
            Do you currently hold another Federal fellowship or traineeship?
        """,
        choices = BINARY_CHOICES, widget = forms.RadioSelect()
    )

    class Meta:
        model = MidwestHighPoweredRocketCompetition
        exclude = (
            'user','status','funds_authorized','authorized_match',
            'other_fellowship','other_fellowship_explain',
            'award_acceptance','interim_report','final_report'
        )

    def __init__(self, *args, **kwargs):
        super(MidwestHighPoweredRocketCompetitionForm, self).__init__(
            *args,**kwargs
        )
        self.fields['team'].queryset = RocketLaunchTeam.objects.annotate(
            count=Count('members')
        ).filter(competition__in=["Midwest High Powered Rocket Competition"]).filter(
            date_created__gte=get_start_date()
        ).exclude(count__gte=settings.ROCKET_LAUNCH_COMPETITION_TEAM_LIMIT).order_by("name")


class MidwestHighPoweredRocketCompetitionUploadsForm(forms.ModelForm):

    class Meta:
        model = MidwestHighPoweredRocketCompetition
        fields = (
            'award_acceptance',
        )


class CollegiateRocketCompetitionForm(forms.ModelForm):

    other_fellowship = forms.TypedChoiceField(
        label="""
            Do you currently hold another Federal fellowship or traineeship?
        """,
        choices = BINARY_CHOICES, widget = forms.RadioSelect()
    )

    class Meta:
        model = CollegiateRocketCompetition
        exclude = (
            'user','status','funds_authorized','authorized_match',
            'other_fellowship','other_fellowship_explain',
            'award_acceptance','interim_report','final_report'
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
            'user','status','funds_authorized','authorized_match',
            'other_fellowship','other_fellowship_explain',
            'award_acceptance','final_report','interim_report','invoice',
            'program_match','payment_information'
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

    other_fellowship = forms.TypedChoiceField(
        label="""
            Do you currently hold another Federal fellowship or traineeship?
        """,
        choices = BINARY_CHOICES, widget = forms.RadioSelect()
    )

    class Meta:
        model = IndustryInternship
        exclude = (
            'user','status','work_plan','funds_authorized','authorized_match',
            'other_fellowship','other_fellowship_explain',
            'award_acceptance','final_report','interim_report',
            'invoice','program_match','payment_information'
        )


class IndustryInternshipUploadsForm(forms.ModelForm):

    class Meta:
        model = IndustryInternship
        fields = (
            'budget','award_acceptance','final_report','interim_report',
            'invoice','program_match','payment_information'
        )
