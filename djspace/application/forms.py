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
#from djtools.fields.validators import MimetypeValidator
from djtools.fields import BINARY_CHOICES

'''
UploadsForms are for the user dashboard where file uploads
take place after the application has been approved and
additional files are required
'''


class HigherEducationInitiativesForm(forms.ModelForm):
    budget = forms.FileField(
        help_text="""
            Note the spend down date requirement in the Announcement of Opportunity.
        """
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
    grants_officer = forms.CharField(
        label = "Grants Officer",
        required = False,
        help_text = '''
            Grants Officer user, if they have registered with this site.
        ''',
    )

    class Meta:
        model = HigherEducationInitiatives
        fields = (
            'project_title','award_type','funds_requested',
            'proposed_match','source_match',
            'past_funding','past_funding_year','anticipating_funding',
            'other_fellowship','other_fellowship_explain',
            'begin_date','end_date','location','synopsis',
            'proposal','budget','intended_program_match',
            'finance_officer_name','finance_officer_title',
            'finance_officer_address',
            'finance_officer_email','finance_officer_phone',
            'grant_officer_name','grant_officer_title','grant_officer_address',
            'grant_officer_email','grant_officer_phone','grants_officer',
            'member_1','member_2','member_3','member_4','member_5',
            'member_6','member_7','member_8','member_9','member_10',
        )


class HigherEducationInitiativesUploadsForm(forms.ModelForm):

    class Meta:
        model = HigherEducationInitiatives
        fields = (
            'award_acceptance','final_report','interim_report',
            'other_file','other_file2','other_file3',
            'invoice','intended_program_match','close_out_finance_document'
        )


class ResearchInfrastructureForm(forms.ModelForm):

    budget = forms.FileField(
        help_text="""
            Note the spend down date requirement in the Announcement of Opportunity.
        """
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
    grants_officer = forms.CharField(
        label = "Grants Officer",
        required = False,
        help_text = '''
            Grants Officer user, if they have registered with this site.
        ''',
    )

    class Meta:
        model = ResearchInfrastructure
        fields = (
            'project_title','award_type','funds_requested',
            'proposed_match','source_match',
            'past_funding','past_funding_year','anticipating_funding',
            'other_fellowship','other_fellowship_explain',
            'begin_date','end_date','location','synopsis',
            'proposal','budget','invoice','intended_program_match',
            'nasa_mission_directorate',
            'nasa_mission_directorate_other',
            'finance_officer_name','finance_officer_title',
            'finance_officer_address',
            'finance_officer_email','finance_officer_phone',
            'grant_officer_name','grant_officer_title','grant_officer_address',
            'grant_officer_email','grant_officer_phone','grants_officer',
            'member_1','member_2','member_3','member_4','member_5',
            'member_6','member_7','member_8','member_9','member_10',
        )


class ResearchInfrastructureUploadsForm(forms.ModelForm):

    class Meta:
        model = ResearchInfrastructure
        fields = (
            'award_acceptance','final_report','interim_report',
            'other_file','other_file2','other_file3',
            'invoice','intended_program_match','close_out_finance_document'
        )


class AerospaceOutreachForm(forms.ModelForm):

    budget = forms.FileField(
        help_text="""
            Note the spend down date requirement in the Announcement of Opportunity.
        """
    )
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
    end_date = forms.DateField(required=True)
    grants_officer = forms.CharField(
        label = "Grants Officer",
        required = False,
        help_text = '''
            Grants Officer user, if they have registered with this site.
        ''',
    )

    class Meta:
        model = AerospaceOutreach
        fields = (
            'project_title','project_category','funds_requested',
            'proposed_match','source_match',
            'past_funding','past_funding_year','anticipating_funding',
            'other_funding','other_funding_explain',
            'begin_date','end_date','location','synopsis',
            'proposal','budget','intended_program_match',
            'nasa_mission_directorate','nasa_mission_directorate_other',
            'finance_officer_name','finance_officer_title',
            'finance_officer_address',
            'finance_officer_email','finance_officer_phone',
            'grant_officer_name','grant_officer_title','grant_officer_address',
            'grant_officer_email','grant_officer_phone','grants_officer',
            'member_1','member_2','member_3','member_4','member_5',
            'member_6','member_7','member_8','member_9','member_10',
        )


class AerospaceOutreachUploadsForm(forms.ModelForm):

    class Meta:
        model = AerospaceOutreach
        fields = (
            'award_acceptance','final_report','interim_report',
            'other_file','other_file2','other_file3',
            'invoice','intended_program_match','close_out_finance_document'
        )


class SpecialInitiativesForm(forms.ModelForm):

    budget = forms.FileField(
        help_text="""
            Note the spend down date requirement in the Announcement of Opportunity.
        """
    )
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
    end_date = forms.DateField(required=True)
    grants_officer = forms.CharField(
        label = "Grants Officer",
        required = False,
        help_text = '''
            Grants Officer user, if they have registered with this site.
        ''',
    )

    class Meta:
        model = SpecialInitiatives
        fields = (
            'project_title','project_category','funds_requested',
            'proposed_match','source_match',
            'past_funding','past_funding_year','anticipating_funding',
            'other_funding','other_funding_explain',
            'begin_date','end_date','location','synopsis',
            'proposal','budget','intended_program_match',
            'nasa_mission_directorate','nasa_mission_directorate_other',
            'finance_officer_name','finance_officer_title',
            'finance_officer_address',
            'finance_officer_email','finance_officer_phone',
            'grant_officer_name','grant_officer_title','grant_officer_address',
            'grant_officer_email','grant_officer_phone','grants_officer',
            'member_1','member_2','member_3','member_4','member_5',
            'member_6','member_7','member_8','member_9','member_10',
        )


class SpecialInitiativesUploadsForm(forms.ModelForm):

    class Meta:
        model = SpecialInitiatives
        fields = (
            'award_acceptance','final_report','interim_report',
            'other_file','other_file2','other_file3',
            'invoice','intended_program_match','close_out_finance_document'
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
            'complete', 'user','status','funded_code','funds_authorized',
            'authorized_match','award_acceptance','final_report',
            'other_file','other_file2','other_file3','interim_report',
            'url1','url2','url3'
        )


class UndergraduateScholarshipUploadsForm(forms.ModelForm):

    class Meta:
        model = UndergraduateScholarship
        fields = (
            'award_acceptance','final_report','interim_report',
            'other_file','other_file2','other_file3',
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
            'complete','user','status','funded_code','funds_authorized',
            'authorized_match','award_acceptance','final_report',
            'other_file','other_file2','other_file3','interim_report',
            'url1','url2','url3'
        )


class StemBridgeScholarshipUploadsForm(forms.ModelForm):

    class Meta:
        model = StemBridgeScholarship
        fields = (
            'award_acceptance','final_report','interim_report',
            'other_file','other_file2','other_file3',
        )


class WomenInAviationScholarshipForm(forms.ModelForm):

    statement = models.FileField(
        upload_to = partial(upload_to_path, 'Statement'),
        validators=FILE_VALIDATORS,
        max_length=255,
        help_text=mark_safe('''
            Maximum two-page statement containing the following:
            <ol style="font-weight:bold;color:#000;list-style-type:upper-alpha;margin-left:25px;">
            <li>interest in aviation</li>
            <li>experience in aviation (coursework, pilot training, etc.)</li>
            <li>benefit of attending the 2020 Women in Aviation conference</li>
            <li>future plan to participate in aviation as a career, hobby, etc./<li>
            </ol> [PDF format]
        ''')
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
        model = WomenInAviationScholarship
        exclude = (
            'complete','user','status','funded_code','funds_authorized',
            'authorized_match','award_acceptance','final_report',
            'other_file','other_file2','other_file3','interim_report',
            'url1','url2','url3'
        )


class WomenInAviationScholarshipUploadsForm(forms.ModelForm):

    class Meta:
        model = WomenInAviationScholarship
        fields = (
            'award_acceptance','final_report','interim_report',
            'other_file','other_file2','other_file3',
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
            'complete','user','status','funded_code','funds_authorized',
            'authorized_match','award_acceptance','final_report',
            'other_file','other_file2','other_file3','interim_report',
            'url1','url2','url3'
        )


class UndergraduateResearchUploadsForm(forms.ModelForm):

    class Meta:
        model = UndergraduateResearch
        fields = (
            'award_acceptance','final_report','interim_report',
            'other_file','other_file2','other_file3',
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
        full-time graduate or professional student
        at one of the Wisconsin Space
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
            'complete','user','status','funded_code','funds_authorized',
            'authorized_match','award_acceptance','final_report',
            'other_file','other_file2','other_file3','interim_report',
            'url1','url2','url3'
        )


class GraduateFellowshipUploadsForm(forms.ModelForm):

    class Meta:
        model = GraduateFellowship
        fields = (
            'award_acceptance','final_report','interim_report',
            'other_file','other_file2','other_file3',
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
        full-time graduate or professional student
        at one of the Wisconsin Space
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
            'complete','user','status','funded_code','funds_authorized',
            'authorized_match','award_acceptance','final_report',
            'other_file','other_file2','other_file3','interim_report',
            'url1','url2','url3'
        )


class ClarkGraduateFellowshipUploadsForm(forms.ModelForm):

    class Meta:
        model = ClarkGraduateFellowship
        fields = (
            'award_acceptance','final_report','interim_report',
            'other_file','other_file2','other_file3',
        )


class HighAltitudeBalloonPayloadForm(forms.ModelForm):

    commit = forms.TypedChoiceField(
        label="""
            Will you be able to commit 32-40 hours/week
            to this 10-week summer experience?
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
            'complete','user','status','funded_code','funds_authorized',
            'authorized_match','award_acceptance','final_report',
            'other_file','other_file2','other_file3','interim_report',
            'url1','url2','url3','team_photo','team_biography'
        )


class HighAltitudeBalloonPayloadUploadsForm(forms.ModelForm):

    class Meta:
        model = HighAltitudeBalloonPayload
        fields = (
            'award_acceptance','final_report','interim_report',
            'other_file','other_file2','other_file3',
            'team_photo','team_biography'
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
            'complete','user','status','commit','funded_code','funds_authorized',
            'authorized_match','award_acceptance','final_report',
            'other_file','other_file2','other_file3','interim_report',
            'url1','url2','url3','team_photo','team_biography'
        )


class HighAltitudeBalloonLaunchUploadsForm(forms.ModelForm):

    class Meta:
        model = HighAltitudeBalloonLaunch
        fields = (
            'award_acceptance','final_report','interim_report',
            'other_file','other_file2','other_file3',
            'team_photo','team_biography'
        )


class RocketLaunchTeamForm(forms.ModelForm):
    '''
    Form that handles the create/update for Rocket Launch Teams
    '''
    uid = forms.CharField(
        required=False, max_length=64, widget=forms.HiddenInput()
    )
    co_advisor = forms.CharField(
        label = "Co-Advisor",
        required = False,
        help_text = '''
            Co-Advisor must be registered for auto-population of this field.
        ''',
    )
    leader = forms.CharField(
        label = "Team Lead",
        required = True,
        help_text = '''
            Team Leads must be registered for auto-population of this field.
        ''',
    )
    grants_officer = forms.CharField(
        label = "Grants Officer",
        required = False,
        help_text = '''
            Grants Officer user, if they have registered with this site.
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
    '''
    other_fellowship = forms.TypedChoiceField(
        label="""
            Do you currently hold another Federal fellowship or traineeship?
        """,
        choices = BINARY_CHOICES, widget = forms.RadioSelect()
    )
    '''

    class Meta:
        model = RocketLaunchTeam
        exclude = (
            'complete','user','status','funded_code','funds_authorized',
            'authorized_match','members','award_acceptance',
            'interim_progress_report','interim_report','team_roster',
            'preliminary_design_report','final_design_report','final_report',
            'flight_demo','lodging_list','proposal',
            'other_file','other_file2','other_file3',
            'critical_design_report','oral_presentation','proceeding_paper',
            'flight_readiness_report','post_flight_performance_report',
            'education_outreach','verified_budget','final_motor_selection',
            'close_out_finance_document','invoice','charges_certification',
            'institutional_w9', 'url1','url2','url3','team_photo','team_biography',
            'virtual_cdr','virtual_pdr','virtual_frr'
        )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(RocketLaunchTeamForm, self).__init__(*args, **kwargs)

    def clean(self):
        '''
        '''
        cd = self.cleaned_data
        cid = cd.get('co_advisor')
        gid = cd.get('grants_officer')
        #uid = cd.get('uid')
        #uid = cd['uid']
        uid = str(self.request.user.id)

        # Assign a User object to grants officer
        if gid:
            if gid == uid:
                self.add_error('grants_officer', "You cannot also be a grants officer")
                cd['grants_officer'] = None
            else:
                try:
                    user = User.objects.get(pk=gid)
                    cd['grants_officer'] = user
                    self.request.session['grants_officer_name'] = u'{}, {}'.format(
                        user.last_name, user.first_name
                    )
                except:
                    self.add_error(
                        'grants_officer', "That User does not exist in the system"
                    )
        else:
            cd['grants_officer'] = None

        # Assign a User object to co-advisor
        if cid:
            if cid == uid:
                self.add_error('co_advisor', "You cannot also be a co-advisor")
                cd['co_advisor'] = None
            else:
                try:
                    user = User.objects.get(pk=cid)
                    cd['co_advisor'] = user
                    self.request.session['co_advisor_name'] = u'{}, {}'.format(
                        user.last_name, user.first_name
                    )
                except:
                    self.add_error(
                        'co_advisor', "That User does not exist in the system"
                    )
        else:
            cd['co_advisor'] = None

        '''
        Assign a User object to team leader
        '''
        lid = cd.get('leader')
        if lid:
            try:
                user = User.objects.get(pk=lid)
                cd['leader'] = user
                self.request.session['leader_name'] = u'{}, {}'.format(
                    user.last_name, user.first_name
                )
            except:
                self.add_error(
                    'leader', "The team leader does not exist in the system"
                )
        else:
            self.add_error(
                'leader', "The team leader does not exist in the system"
            )

        return cd


class RocketLaunchTeamUploadsForm(forms.ModelForm):

    class Meta:
        model = RocketLaunchTeam
        fields = (
            'award_acceptance','interim_progress_report',
            'preliminary_design_report','final_design_report',
            'flight_demo','lodging_list','openrocketrocksim',
            'other_file','other_file2','other_file3',
            'critical_design_report','oral_presentation',
            'post_flight_performance_report','education_outreach',
            'flight_readiness_report','proceeding_paper','proposal',
            'budget','verified_budget','close_out_finance_document',
            'invoice','charges_certification','institutional_w9',
            'virtual_cdr','virtual_pdr','virtual_frr',
            'team_photo','team_biography'
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
    '''
    media_release = forms.FileField(
        max_length=768, help_text="PDF format"
    )
    irs_w9= forms.FileField(
        label="IRS W9", help_text="PDF format"
    )
    '''

    class Meta:
        model = FirstNationsRocketCompetition
        exclude = (
            'complete','user','status','funded_code','funds_authorized',
            'authorized_match','award_acceptance','interim_report',
            'final_report','other_file','other_file2','other_file3',
            'url1','url2','url3'
        )


    def __init__(self, *args, **kwargs):
        super(FirstNationsRocketCompetitionForm, self).__init__(
            *args,**kwargs
        )
        self.fields['team'].queryset = RocketLaunchTeam.objects.filter(
            competition__contains="First Nations"
        ).filter(date_created__gte=get_start_date()).order_by("name")
        '''
        instance = kwargs.get('instance', None)
        if instance:
            self.fields['media_release'].initial = instance.get_media_release()
        if instance:
            self.fields['irs_w9'].initial = instance.get_irs_w9()
        '''


class FirstNationsRocketCompetitionUploadsForm(forms.ModelForm):
    """
    WSGC have removed the requirement for Award Acceptance letter but
    we will keep this form class in place for when they decide to go
    back to requiring it.
    """

    class Meta:
        model = FirstNationsRocketCompetition
        fields = (
            'award_acceptance','other_file','other_file2','other_file3',
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
    '''
    media_release = forms.FileField(
        max_length=768, help_text="PDF format"
    )
    irs_w9= forms.FileField(
        label="IRS W9", help_text="PDF format"
    )
    '''

    class Meta:
        model = MidwestHighPoweredRocketCompetition
        exclude = (
            'complete','user','status','funded_code','funds_authorized',
            'authorized_match','award_acceptance','interim_report',
            'final_report','other_file','other_file2','other_file3',
            'url1','url2','url3'
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
        '''
        instance = kwargs.get('instance', None)
        if instance:
            self.fields['media_release'].initial = instance.get_media_release()
            self.fields['irs_w9'].initial = instance.get_irs_w9()
        '''


class MidwestHighPoweredRocketCompetitionUploadsForm(forms.ModelForm):

    class Meta:
        model = MidwestHighPoweredRocketCompetition
        fields = (
            'award_acceptance','other_file','other_file2','other_file3',
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
    '''
    media_release = forms.FileField(
        max_length=768, help_text="PDF format"
    )
    irs_w9= forms.FileField(
        label="IRS W9", help_text="PDF format"
    )
    '''

    class Meta:
        model = CollegiateRocketCompetition
        exclude = (
            'complete','user','status','funded_code','funds_authorized',
            'authorized_match','award_acceptance','interim_report',
            'final_report','other_file','other_file2','other_file3',
            'url1','url2','url3'
        )


    def __init__(self, *args, **kwargs):
        super(CollegiateRocketCompetitionForm, self).__init__(
            *args,**kwargs
        )
        self.fields['team'].queryset = RocketLaunchTeam.objects.annotate(
            count=Count('members')
        ).filter(competition__in=["Collegiate Rocket Competition"]).filter(
            date_created__gte=get_start_date()
        ).exclude(
            count__gte=settings.ROCKET_LAUNCH_COMPETITION_TEAM_LIMIT
        ).order_by("name")
        '''
        instance = kwargs.get('instance', None)
        if instance:
            self.fields['media_release'].initial = instance.get_media_release()
            self.fields['irs_w9'].initial = instance.get_irs_w9()
        '''


class CollegiateRocketCompetitionUploadsForm(forms.ModelForm):

    class Meta:
        model = CollegiateRocketCompetition
        fields = (
            'award_acceptance','other_file','other_file2','other_file3',
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
    program_acceptance = forms.TypedChoiceField(
        label = "Has your team applied and been accepted into the program?",
        choices = BINARY_CHOICES, widget = forms.RadioSelect()
    )
    end_date = forms.DateField(required=True)

    class Meta:
        model = NasaCompetition
        exclude = (
            'complete','user','status','funded_code','funds_authorized',
            'authorized_match','award_acceptance','final_report',
            'other_file','other_file2','other_file3',
            'interim_report','invoice','intended_program_match',
            'close_out_finance_document','url1','url2','url3',
            'team_photo','team_biography'
        )

    def clean(self):
        """
        Check "other" fields if need be
        """
        cd = self.cleaned_data

        if cd.get("competition_type") == "Other":
            if cd.get("competition_type_other") == "":
                self.add_error('competition_type_other', "Required field")

        if cd.get("facility_name") == "Other":
            if cd.get("facility_name_other") == "":
                self.add_error('facility_name_other', "Required field")

        return cd


class NasaCompetitionUploadsForm(forms.ModelForm):

    class Meta:
        model = NasaCompetition
        fields = (
            'award_acceptance','final_report','interim_report','invoice',
            'intended_program_match','close_out_finance_document',
            'other_file','other_file2','other_file3',
            'team_photo','team_biography'
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

    class Meta:
        model = IndustryInternship
        exclude = (
            'complete','user','status','funded_code','work_plan',
            'authorized_match','award_acceptance','final_report',
            'other_file','other_file2','other_file3',
            'interim_report','invoice','intended_program_match',
            'close_out_finance_document','funds_authorized',
            'url1','url2','url3'
        )


class IndustryInternshipUploadsForm(forms.ModelForm):

    class Meta:
        model = IndustryInternship
        fields = (
            'award_acceptance','final_report','interim_report',
            'other_file','other_file2','other_file3',
            'invoice','intended_program_match','close_out_finance_document'
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
    AerospaceOutreach = forms.CharField(
        required=False, max_length=64, widget=forms.HiddenInput()
    )
    HigherEducationInitiatives = forms.CharField(
        required=False, max_length=64, widget=forms.HiddenInput()
    )
    IndustryInternship = forms.CharField(
        required=False, max_length=64, widget=forms.HiddenInput()
    )
    NasaCompetition = forms.CharField(
        required=False, max_length=64, widget=forms.HiddenInput()
    )
    ResearchInfrastructure = forms.CharField(
        required=False, max_length=64, widget=forms.HiddenInput()
    )
    SpecialInitiatives = forms.CharField(
        required=False, max_length=64, widget=forms.HiddenInput()
    )

    class Meta:
        model = ProfessionalProgramStudent
        fields = (
            'program','mentor','award_acceptance','past_funding',
            'past_funding_year','anticipating_funding'
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
            try:
                user = User.objects.get(pk=mid)
                cd['mentor'] = user
            except:
                self.add_error(
                    'mentor', "That User does not exist in the system"
                )
        else:
            self.add_error('mentor', "Required field")

        return cd.get('mentor')


class ProfessionalProgramStudentUploadsForm(forms.ModelForm):

    class Meta:
        model = HigherEducationInitiatives
        fields = (
            'award_acceptance','interim_report','final_report',
            'other_file','other_file2','other_file3',
        )
