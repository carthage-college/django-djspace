# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from django.db.models.signals import pre_delete
from django.core.validators import FileExtensionValidator

from djspace.core.models import Base, BaseModel
from djspace.registration.choices import WSGC_SCHOOL
from djspace.core.utils import upload_to_path
from djspace.core.utils import get_term
from djspace.core.models import PHOTO_VALIDATORS, ALLOWED_EXTENSIONS

from djtools.fields import BINARY_CHOICES, SALUTATION_TITLES, STATE_CHOICES
from djtools.fields import GENDER_CHOICES, TODAY

from uuid import uuid4
from functools import partial

import re

YEAR_2 = int(TODAY.strftime('%y'))
if TODAY.month >= settings.GRANT_CYCLE_START_MES:
    YEAR_2 = YEAR_2 + 1

FILE_VALIDATORS = [
    FileExtensionValidator(allowed_extensions=ALLOWED_EXTENSIONS)
]
DIRECTORATE_CHOICES = (
    (
        'Aeronautics Research','Aeronautics Research'
    ),
    (
        'Human Exploration and Operations Mission Directorate',
        'Human Exploration and Operations Mission Directorate'
    ),
    ('Science','Science'),
    ('Space Technology','Space Technology'),
    ('Other','Other')
)
GRAVITY_TRAVEL = (
    ('gravity','Reduced Gravity'),
    ('travel','Student Travel')
)
TIME_FRAME = (
    ('Summer','Summer'),
    ('Summer and fall','Summer and fall'),
    ('Fall','Fall'),
    ('Spring','Spring'),
    ('Summer, fall, and spring','Summer, fall, and spring'),
    ('Fall and spring','Fall and spring')
)
PROJECT_CATEGORIES = (
    (
        'Pre-College Program (Formal Education Outreach - K-12)',
        'Pre-College Program (Formal Education Outreach - K-12)'
    ),
    (
        'Informal Education Program (Museums, Planetariums, etc.)',
        'Informal Education Program (Museums, Planetariums, etc.)'
    )
)
ACADEMIC_INSTITUTIONS = (
    (
        'Two-year Academic Institution Opportunity (Fall)',
        'Two-year Academic Institution Opportunity (Fall)'
    ),
    (
        'All Academic Institution Opportunity (Spring)',
        'All Academic Institution Opportunity (Spring)'
    ),
    (
        'STEM Bridge','STEM Bridge'
    )
)
INDUSTRY_AWARD_TYPES = (
    (
        'Industry Internship: $5000 award with a required 1:1 match',
        'Industry Internship: $5000 award with a required 1:1 match'
    ),
    (
        'Industry Internship: $5000 award with an optional match',
        'Industry Internship: $5000 award with an optional match'
    ),
    (
        'Internship/Apprenticeship: $0.00 Award with full match',
        'Internship/Apprenticeship:  $0.00 Award with full match'
    ),
    (
        'Technical Apprenticeship: $2500 for two-year schools with a 1:1 match',
        'Technical Apprenticeship: $2500 for two-year schools with a 1:1 match'
    ),
    (
        'Technical Apprenticeship:  $2500 for two-year schools with an optional match.',
        'Technical Apprenticeship:  $2500 for two-year schools with an optional match.'
    ),
)
UNDERGRADUATE_RESEARCH_AWARD_TYPES = (
    (
        'Summer Research:  Up to $4000',
        'Summer Research:  Up to $4000'
    ),
    (
        'Academic-Year Research:  Up to $4000',
        'Academic-Year Research:  Up to $4000'
    )
)
EDUCATION_INITIATIVES_AWARD_TYPES = (
    ('Major Award: $5000-$10000','Major Award: $5000-$10000'),
    ('Minor Award:  Up to $5000','Minor Award:  Up to $5000')
)
DISCIPLINES = (
    ('Engineering','Engineering'),
    ('Biology','Biology'),
    ('Technical (2 year)','Technical (2 year)'),
    ('Other','Other')
)
NASA_COMPETITION_TYPES = (
    ('HASP','HASP'),
    ('Micro-G/NExT','Micro-G/NExT'),
    ('Robotic Mining','Robotic Mining'),
    ('RockSat','RockSat'),
    ('XHab','XHab'),
    ('Other','Other')
)
NASA_CENTER_CHOICES = (
    ('Ames Research Center','Ames Research Center'),
    ('Armstrong Flight Research Center','Armstrong Flight Research Center'),
    ('Glenn Research Center','Glenn Research Center'),
    ('Goddard Space Flight Center','Goddard Space Flight Center'),
    ('Jet Propulsion Laboratory','Jet Propulsion Laboratory'),
    ('Johnson Space Center','Johnson Space Center'),
    ('Kennedy Space Center','Kennedy Space Center'),
    ('Langley Research Center','Langley Research Center'),
    ('Marshall Space Flight Center','Marshall Space Flight Center'),
    ('Stennis Space Center','Stennis Space Center'),
    ('Wallops Flight Facility','Wallops Flight Facility'),
    ('Other','Other')
)
NASA_COMPETITION_AWARD_TYPES = (
    ('Project award','Project award'),
    ('Travel award','Travel award')
)
FIRST_NATIONS_ROCKET_COMPETITIONS = (
    ('Tribal Challenge','Tribal Challenge'),
    ('AISES Challenge','AISES Challenge'),
)
ROCKET_COMPETITIONS = (
    ("Collegiate Rocket Competition", "Collegiate Rocket Competition"),
    ("First Nations AISES", "First Nations AISES"),
    ("First Nations Tribal", "First Nations Tribal"),
    (
        "Midwest High Powered Rocket Competition",
        "Midwest High Powered Rocket Competition"
    )
)
ROCKET_LAUNCH_COMPETITION_WITH_LIMIT = [
    "Midwest High Powered Rocket Competition",
    "Collegiate Rocket Competition"
]
PROFESSIONAL_PROGRAMS = [
    "aerospaceoutreach",
    "highereducationinitiatives",
    "industryinternship",
    "nasacompetition",
    "researchinfrastructure",
    "specialinitiatives",
]
STUDENT_PROFESSIONAL_PROGRAMS = (
    ('AerospaceOutreach', 'Aerospace Outreach'),
    ('CaNOP', 'CaNOP'),
    ('HigherEducationInitiatives', 'Higher Education Initiatives'),
    ('IndustryInternship', 'Industry Internship'),
    ('MicroPropellantGauging','Micro-Propellant Gauging'),
    ('NasaCompetition', 'NASA Competition'),
    ('NasaInternship', 'NASA Internship'),
    ('ResearchInfrastructure', 'Research Infrastructure'),
    ('SpecialInitiatives', 'Special Initiatives')
)

# only used at UI level
ROCKET_COMPETITIONS_EXCLUDE = [
    "midwesthighpoweredrocketcompetition",
    "collegiaterocketcompetition",
    "firstnationsrocketcompetition"
]


class EducationInitiatives(BaseModel):

    class Meta:
        abstract = True

    # core
    project_title = models.CharField(
        "Title of project", max_length=255
    )
    funds_requested = models.IntegerField(help_text="In dollars")
    funds_authorized = models.IntegerField(
        null = True, blank = True,
        help_text="In Dollars"
    )
    proposed_match = models.IntegerField(
        "Proposed match (1:1 mimimum)(in $)",
    )
    authorized_match = models.IntegerField(
        null = True, blank = True
    )
    source_match = models.CharField(
        "Source(s) of match", max_length=255
    )
    other_fellowship = models.CharField(
        "Do you currently hold another Federal fellowship or traineeship?",
        max_length=4,
        choices=BINARY_CHOICES,
    )
    other_fellowship_explain = models.CharField(
        """
            If yes, please provide the funding source and the
            funding expiration date.
        """,
        max_length=255,
        null = True, blank = True
    )
    begin_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    location = models.CharField(
        "Location of project", max_length=255
    )
    synopsis = models.TextField(
        help_text = '''
            Please include a short synopsis of your project
            (no more than 200 characters) outlining its purpose
            in terms understandable by the general reader.
            If your project is selected for funding, this
            wording will be used on our website.
        '''
    )
    proposal = models.FileField(
        upload_to = partial(upload_to_path, 'Proposal'),
        validators=FILE_VALIDATORS,
        max_length=768,
        help_text="PDF format"
    )
    budget = models.FileField(
        upload_to = partial(upload_to_path, 'Budget'),
        validators=FILE_VALIDATORS,
        max_length=768,
        help_text="[PDF format]"
    )
    student_1 = models.CharField(
        max_length=128,
        null = True, blank = True
    )
    student_2 = models.CharField(
        max_length=128,
        null = True, blank = True
    )
    student_3 = models.CharField(
        max_length=128,
        null = True, blank = True
    )
    student_4 = models.CharField(
        max_length=128,
        null = True, blank = True
    )
    student_5 = models.CharField(
        max_length=128,
        null = True, blank = True
    )
    finance_officer_name = models.CharField(
        "Name", max_length=128
    )
    finance_officer_title = models.CharField(
        "Title", max_length=128
    )
    finance_officer_address = models.TextField("Address")
    finance_officer_email = models.EmailField("Email")
    finance_officer_phone = models.CharField(
        verbose_name='Phone number',
        max_length=12,
        help_text="Format: XXX-XXX-XXXX"
    )
    grant_officer_name = models.CharField(
        "Name",
        max_length=128
    )
    grant_officer_address = models.TextField("Address")
    grant_officer_email = models.EmailField("Email")
    grant_officer_phone = models.CharField(
        verbose_name='Phone number',
        max_length=12,
        help_text="Format: XXX-XXX-XXXX"
    )
    invoice = models.FileField(
        upload_to = partial(upload_to_path, 'Invoice'),
        validators=FILE_VALIDATORS,
        max_length=768,
        null=True, blank=True,
        help_text="PDF format"
    )
    intended_program_match = models.FileField(
        upload_to = partial(upload_to_path, 'Intended_Program_Match'),
        validators=FILE_VALIDATORS,
        max_length=768,
        null=True, blank=True,
        help_text="PDF format"
    )
    close_out_finance_document = models.FileField(
        upload_to = partial(upload_to_path, 'Closeout_Finance_Document'),
        validators=FILE_VALIDATORS,
        max_length=768,
        null=True, blank=True,
        help_text="PDF format"
    )

    def required_files(self):
        '''
        used when building a tarball of required files
        '''
        return ['proposal','budget']

    # timestamp methods are for UI level display
    def budget_timestamp(self):
        return self.get_file_timestamp("budget")

    def __unicode__(self):
        return self.project_title


class HigherEducationInitiatives(EducationInitiatives):

    award_type = models.CharField(
        "Award",
        max_length = 128,
        choices = EDUCATION_INITIATIVES_AWARD_TYPES,
        help_text = """
            Select the opportunity to which the proposal is being submitted.
        """
    )

    def __unicode__(self):
        return self.project_title

    def get_application_type(self):
        return "Higher Education Initiatives"

    def get_slug(self):
        return "higher-education-initiatives"

    def get_code(self):
        award_type = "MNR"
        if "Major" in self.award_type:
            award_type = "MJR"
        return "HEI{}_{}".format(YEAR_2,award_type)

    @models.permalink
    def get_absolute_url(self):
        return ('application_update', [self.get_slug(), str(self.id)])

    class Meta:
        verbose_name_plural = "Higher Education Initiatives"


class ResearchInfrastructure(EducationInitiatives):

    award_type = models.CharField(
        "Award",
        max_length = 128,
        choices = EDUCATION_INITIATIVES_AWARD_TYPES,
        help_text = """
            Select the opportunity to which the proposal is being submitted.
        """
    )
    nasa_mission_directorate = models.CharField(
        "NASA Mission directorate",
        max_length=128,
        choices=DIRECTORATE_CHOICES,
        help_text='''
            See NASA's
            <a href="https://www.nasa.gov/offices/education/missions/"
              target="_blank">
                Mission Directorates Education and Outreach
            </a> page for more information.
        '''
    )
    nasa_mission_directorate_other = models.CharField(
        "Other",
        max_length = 128,
        null = True, blank = True,
        help_text = '''
            If you have choosen "Other" in the field above,
            please identify the NASA Mission Directorate in which you are
            requesting funds to participate.
        '''
    )

    def get_code(self):
        award_type = "MNR"
        if "Major" in self.award_type:
            award_type = "MJR"
        return "RIP{}_{}".format(YEAR_2,award_type)

    def __unicode__(self):
        return self.project_title

    def get_application_type(self):
        return "Research Infrastructure"

    def get_slug(self):
        return "research-infrastructure"

    @models.permalink
    def get_absolute_url(self):
        return ('application_update', [self.get_slug(), str(self.id)])

    class Meta:
        verbose_name_plural = "Research Infrastructure"


class AerospaceOutreach(EducationInitiatives):

    project_category = models.CharField(
        max_length=128,
        choices=PROJECT_CATEGORIES
    )
    other_funding = models.CharField(
        "Are you seeking other WSGC funding for this project?",
        max_length=4,
        choices=BINARY_CHOICES,
    )
    other_funding_explain = models.CharField(
        "If yes, please explain",
        max_length=255,
        null = True, blank = True
    )
    nasa_mission_directorate = models.CharField(
        "NASA Mission directorate",
        max_length=128,
        choices=DIRECTORATE_CHOICES,
        help_text='''
            See NASA's
            <a href="https://www.nasa.gov/offices/education/missions/"
              target="_blank">
                Mission Directorates Education and Outreach
            </a> page for more information.
        '''
    )
    nasa_mission_directorate_other = models.CharField(
        "Other",
        max_length = 128,
        null = True, blank = True,
        help_text = '''
            If you have choosen "Other" in the field above,
            please identify the NASA Mission Directorate in which you are
            requesting funds to participate.
        '''
    )

    def __unicode__(self):
        return self.project_title

    def get_application_type(self):
        return "Aerospace Outreach"

    def get_slug(self):
        return "aerospace-outreach"

    def get_code(self):
        project_category = "IE"
        if "K-12" in self.project_category:
            project_category = "K12"
        return "AOP{}_{}".format(YEAR_2, project_category)

    @models.permalink
    def get_absolute_url(self):
        return ('application_update', [self.get_slug(), str(self.id)])

    class Meta:
        verbose_name_plural = "Aerospace Outreach"


class SpecialInitiatives(EducationInitiatives):

    project_category = models.CharField(
        max_length=128,
        choices=PROJECT_CATEGORIES
    )
    other_funding = models.CharField(
        "Are you seeking other WSGC funding for this project?",
        max_length=4,
        choices=BINARY_CHOICES,
    )
    other_funding_explain = models.CharField(
        "If yes, please explain",
        max_length=255,
        null = True, blank = True
    )
    nasa_mission_directorate = models.CharField(
        "NASA Mission directorate",
        max_length=128,
        choices=DIRECTORATE_CHOICES,
        help_text='''
            See NASA's
            <a href="https://www.nasa.gov/offices/education/missions/"
              target="_blank">
                Mission Directorates Education and Outreach
            </a> page for more information.
        '''
    )
    nasa_mission_directorate_other = models.CharField(
        "Other",
        max_length = 128,
        null = True, blank = True,
        help_text = '''
            If you have choosen "Other" in the field above,
            please identify the NASA Mission Directorate in which you are
            requesting funds to participate.
        '''
    )

    def __unicode__(self):
        return self.project_title

    def get_application_type(self):
        return "Special Initiatives"

    def get_slug(self):
        return "special-initiatives"

    def get_code(self):
        project_category = "IE"
        if "K-12" in self.project_category:
            project_category = "K12"
        return "SIP{}_{}".format(YEAR_2,project_category)

    @models.permalink
    def get_absolute_url(self):
        return ('application_update', [self.get_slug(), str(self.id)])

    class Meta:
        verbose_name_plural = "Special Initiatives"


class RocketLaunchTeam(BaseModel):
    # core
    name = models.CharField(
        "Team name",
        max_length=255
    )
    co_advisor = models.ForeignKey(
        User,
        null = True, blank = True,
        verbose_name="Co-Advisor",
        related_name="rocket_launch_team_co_advisor",
    )
    leader = models.ForeignKey(
        User,
        verbose_name="Team lead",
        related_name="rocket_launch_team_leader",
    )
    members = models.ManyToManyField(
        User, related_name="rocket_launch_team_members"
    )
    industry_mentor_name = models.CharField(
        max_length=128,
        null = True, blank = True,
        help_text="""
            NOTE: Only required for the Collegiate Rocket Competition
            and the Midwest High-Powered Rocket Competition
        """
    )
    industry_mentor_email = models.EmailField(
        max_length=128,
        null = True, blank = True,
        help_text="""
            NOTE: Only required for the Collegiate Rocket Competition
            and the Midwest High-Powered Rocket Competition
        """
    )
    intent_compete = models.TextField(
        "Notification of Intent to Compete"
    )
    other_fellowship = models.CharField(
        "Do you currently hold another Federal fellowship or traineeship?",
        max_length=4,
        choices=BINARY_CHOICES,
    )
    other_fellowship_explain = models.CharField(
        """
            If yes, please provide the funding source and the
            funding expiration date.
        """,
        max_length=255,
        null = True, blank = True
    )
    team_roster = models.TextField(
        "Team Roster",
        help_text="""
            Maximum 6 members, except for First Nations competitions, which
            can have unlimited team members
        """
    )
    # meta
    competition = models.CharField(
        choices = ROCKET_COMPETITIONS,
        max_length=128
    )
    # files
    proposal = models.FileField(
        upload_to = partial(upload_to_path, 'Proposal'),
        validators=FILE_VALIDATORS,
        max_length=768,
        null=True, blank=True,
        help_text="PDF format"
    )
    budget = models.FileField(
        upload_to = partial(upload_to_path, 'Budget'),
        validators=FILE_VALIDATORS,
        max_length=768,
        null=True, blank=True,
        help_text="""
            Rocket supplies and travel. Only required for the
            Midwest High Powered Rocket Competition. [PDF format]
        """
    )
    verified_budget = models.FileField(
        upload_to = partial(upload_to_path, 'Verified_Budget'),
        validators=FILE_VALIDATORS,
        max_length=768,
        null=True, blank=True,
        help_text="PDF format"
    )
    invoice = models.FileField(
        upload_to = partial(upload_to_path, 'Invoice'),
        validators=FILE_VALIDATORS,
        max_length=768,
        null=True, blank=True,
        help_text="PDF format"
    )
    close_out_finance_document = models.FileField(
        upload_to = partial(upload_to_path, 'Closeout_Finance_Document'),
        validators=FILE_VALIDATORS,
        max_length=768,
        null=True, blank=True,
        help_text="PDF format"
    )
    charges_certification = models.FileField(
        upload_to = partial(upload_to_path, 'Charges_Certification'),
        validators=FILE_VALIDATORS,
        max_length=768,
        null=True, blank=True,
        help_text="PDF format"
    )
    institutional_w9 = models.FileField(
        upload_to = partial(upload_to_path, 'Institutional_W9'),
        validators=FILE_VALIDATORS,
        max_length=768,
        null=True, blank=True,
        help_text="PDF format"
    )
    interim_progress_report = models.FileField(
        "Critical Design Report",
        upload_to = partial(upload_to_path, ' Critical_Design_Report'),
        validators=FILE_VALIDATORS,
        max_length=768,
        null=True, blank=True,
        help_text="PDF format"
    )
    virtual_cdr = models.FileField(
        "CDR - Virtual Presentation",
        upload_to = partial(upload_to_path, 'VCDR'),
        max_length=768,
        null=True, blank=True,
        help_text="Power point"
    )
    preliminary_design_report = models.FileField(
        "Preliminary Design Review",
        upload_to = partial(upload_to_path, 'PDR'),
        validators=FILE_VALIDATORS,
        max_length=768,
        null=True, blank=True,
        help_text="PDF format"
    )
    virtual_pdr = models.FileField(
        "PDR - Virtual Presentation",
        upload_to = partial(upload_to_path, 'VPDR'),
        max_length=768,
        null=True, blank=True,
        help_text="Power point"
    )
    final_design_report = models.FileField(
        upload_to = partial(upload_to_path, 'FDR'),
        validators=FILE_VALIDATORS,
        max_length=768,
        null=True, blank=True,
        help_text="PDF format"
    )
    flight_demo = models.CharField(
        max_length=768,
        null=True, blank=True,
        help_text="URL where your video is located"
    )
    final_motor_selection = models.TextField(
        "Motor Selection",
        null=True, blank=True,
        help_text="""
            If you do not have a motor selected at this time,
            leave this field blank, and update your application
            when you have a final motor selection.
        """
    )
    lodging_list = models.FileField(
        upload_to = partial(upload_to_path, 'Lodging_List'),
        validators=FILE_VALIDATORS,
        max_length=768,
        null=True, blank=True,
        help_text="PDF format"
    )
    critical_design_report = models.FileField(
        "Critical Design Review",
        upload_to = partial(upload_to_path, 'CDR'),
        validators=FILE_VALIDATORS,
        max_length=768,
        null=True, blank=True,
        help_text="PDF format"
    )
    oral_presentation = models.FileField(
        upload_to = partial(upload_to_path, 'PPT'),
        max_length=768,
        null=True, blank=True,
        help_text="Power point"
    )
    post_flight_performance_report = models.FileField(
        "Post Launch Assessment Review",
        upload_to = partial(upload_to_path, 'PFPR'),
        validators=FILE_VALIDATORS,
        max_length=768,
        null=True, blank=True,
        help_text="PDF format"
    )
    education_outreach = models.FileField(
        upload_to = partial(upload_to_path, 'Education_Outreach'),
        validators=FILE_VALIDATORS,
        max_length=768,
        null=True, blank=True,
        help_text="PDF format"
    )
    flight_readiness_report = models.FileField(
        "Flight Readiness Review",
        upload_to = partial(upload_to_path, 'FRR'),
        validators=FILE_VALIDATORS,
        max_length=768,
        null=True, blank=True,
        help_text="PDF format"
    )
    virtual_frr = models.FileField(
        "FRR - Virtual Presentation",
        upload_to = partial(upload_to_path, 'VFRR'),
        max_length=768,
        null=True, blank=True,
        help_text="Power point"
    )
    proceeding_paper = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Rocket Launch Team (NOI)'
        verbose_name_plural = 'Rocket Launch Team (NOI)'

    def __unicode__(self):
        return u"{}".format(self.name)

    def get_application_type(self):
        return "Rocket Launch Team"

    def get_slug(self):
        return "rocket-launch-team"

    def get_code(self):
        return "RLT{}".format(YEAR_2)

    def get_file_path(self):
        return "files/applications"

    def get_team_members(self):
        team = None
        if self.competition == "Collegiate Rocket Competition":
            team = self.collegiate_rocket_competition
        elif self.competition == "Midwest High Powered Rocket Competition":
            team = self.midwest_high_powered_rocket_competition
        elif "First Nations" in self.competition:
            team = self.first_nations_rocket_competition
        return team

    def get_file_name(self):

        if self.competition == "Collegiate Rocket Competition":
            code = "CRL{}".format(YEAR_2)
        elif self.competition == "Midwest High Powered Rocket Competition":
            code = "MRL{}".format(YEAR_2)
        elif "First Nations" in self.competition:
            if self.competition == "First Nations AISES":
                suffix = "AISES"
            else:
                suffix = "Tribal"
            code = "FNL{}_{}".format(YEAR_2, suffix)
        # replace anything that is not a word character with a dash
        team_name = re.sub(r'[^a-zA-Z0-9]', '-', self.name)
        school_name = re.sub(
            r'[^a-zA-Z0-9]', '-',
            self.user.profile.get_registration().wsgc_affiliate.name
        )
        return u'{}_{}_{}_{}.{}'.format(
            code, team_name, school_name,
            self.leader.last_name, self.leader.first_name
        )

    @models.permalink
    def get_absolute_url(self):
        return ('application_update', [self.get_slug(), str(self.id)])

    def required_files(self):
        '''
        used when building a tarball of required files
        '''
        return [
            'budget'
        ]

    # timestamp methods are for UI level display
    def budget_timestamp(self):
        return self.get_file_timestamp("budget")

    def proposal_timestamp(self):
        return self.get_file_timestamp('proposal')

    def interim_progress_report_timestamp(self):
        return self.get_file_timestamp("interim_progress_report")

    def preliminary_design_report_timestamp(self):
        return self.get_file_timestamp("preliminary_design_report")

    def final_design_report_timestamp(self):
        return self.get_file_timestamp("final_design_report")

    def final_motor_selection_timestamp(self):
        return self.get_file_timestamp("final_motor_selection")

    def lodging_list_timestamp(self):
        return self.get_file_timestamp("lodging_list")

    def critical_design_report_timestamp(self):
        return self.get_file_timestamp("critical_design_report")

    def oral_presentation_timestamp(self):
        return self.get_file_timestamp("oral_presentation")

    def post_flight_performance_report_timestamp(self):
        return self.get_file_timestamp("post_flight_performance_report")

    def education_outreach_timestamp(self):
        return self.get_file_timestamp("education_outreach")

    def flight_readiness_report_timestamp(self):
        return self.get_file_timestamp("flight_readiness_report")

    def institutional_w9_timestamp(self):
        return self.get_file_timestamp("institutional_w9")

    def virtual_cdr_timestamp(self):
        return self.get_file_timestamp('virtual_cdr')

    def virtual_pdr_timestamp(self):
        return self.get_file_timestamp('virtual_pdr')

    def virtual_frr_timestamp(self):
        return self.get_file_timestamp('virtual_frr')


class MidwestHighPoweredRocketCompetition(BaseModel):

    # core
    team = models.ForeignKey(
        RocketLaunchTeam,
        related_name="midwest_high_powered_rocket_competition"
    )
    cv = models.FileField(
        "Résumé",
        upload_to = partial(upload_to_path, 'CV'),
        validators=FILE_VALIDATORS,
        max_length=768,
        help_text="PDF format"
    )
    past_participation = models.CharField(
        "Have you previously participated in Collegiate Rocket Launch?",
        max_length=4,
        choices=BINARY_CHOICES
    )
    prior_experience = models.TextField(
        "Prior Rocket Experience",
        help_text="""
            Team experience, leadership experience,
            project experience, hands on experience.
        """
    )
    other_fellowship = models.CharField(
        "Do you currently hold another Federal fellowship or traineeship?",
        max_length=4,
        choices=BINARY_CHOICES
    )
    other_fellowship_explain = models.CharField(
        """
            If yes, please provide the funding source and the
            funding expiration date.
        """,
        max_length=255,
        null = True, blank = True
    )

    def __unicode__(self):
        return "Midwest High-Powered Rocket Competition"

    def get_application_type(self):
        return "Midwest High-Powered Rocket Competition"

    def get_slug(self):
        return "midwest-high-powered-rocket-competition"

    def get_code(self):
        return "MRL{}".format(YEAR_2)

    def get_file_name(self):
        team_name = re.sub(r'[^a-zA-Z0-9]', '-', self.team.name)
        school_name = re.sub(
            r'[^a-zA-Z0-9]', '-',
            self.team.user.profile.get_registration().wsgc_affiliate.name
        )
        return u'{}_{}_{}_{}.{}'.format(
            self.get_code(), team_name, school_name,
            self.user.last_name, self.user.first_name
        )

    def required_files(self):
        '''
        used when building a tarball of required files
        '''
        return ['cv']

    @models.permalink
    def get_absolute_url(self):
        return ('application_update', [self.get_slug(), str(self.id)])


class CollegiateRocketCompetition(BaseModel):

    # core
    team = models.ForeignKey(
        RocketLaunchTeam,
        related_name="collegiate_rocket_competition"
    )
    cv = models.FileField(
        "Résumé",
        upload_to = partial(upload_to_path, 'CV'),
        validators=FILE_VALIDATORS,
        max_length=768,
        help_text="PDF format"
    )
    prior_experience = models.TextField(
        "Prior Rocket Experience",
        help_text="""
            Team experience, leadership experience,
            project experience, hands on experience.
        """
    )
    other_fellowship = models.CharField(
        "Do you currently hold another Federal fellowship or traineeship?",
        max_length=4,
        choices=BINARY_CHOICES,
    )
    other_fellowship_explain = models.CharField(
        """
            If yes, please provide the funding source and the
            funding expiration date.
        """,
        max_length=255,
        null = True, blank = True
    )

    def __unicode__(self):
        return "Collegiate Rocket Competition"

    def get_application_type(self):
        return "Collegiate Rocket Competition"

    def get_slug(self):
        return "collegiate-rocket-competition"

    def get_code(self):
        return "CRL{}".format(YEAR_2)

    def get_file_name(self):
        team_name = re.sub(r'[^a-zA-Z0-9]', '-', self.team.name)
        school_name = re.sub(
            r'[^a-zA-Z0-9]', '-',
            self.team.user.profile.get_registration().wsgc_affiliate.name
        )
        return u'{}_{}_{}_{}.{}'.format(
            self.get_code(), team_name, school_name,
            self.user.last_name, self.user.first_name
        )

    def required_files(self):
        '''
        used when building a tarball of required files
        '''
        return ['cv']

    @models.permalink
    def get_absolute_url(self):
        return ('application_update', [self.get_slug(), str(self.id)])


class FirstNationsRocketCompetition(BaseModel):

    # core
    team = models.ForeignKey(
        RocketLaunchTeam,
        related_name="first_nations_rocket_competition"
    )
    competition = models.CharField(
        "Rocket Competition",
        max_length=128,
        choices=FIRST_NATIONS_ROCKET_COMPETITIONS
    )
    prior_experience = models.TextField(
        "Prior Rocket Experience"
    )

    def __unicode__(self):
        return "First Nations Rocket Competition"

    def get_application_type(self):
        return "First Nations Rocket Competition"

    def get_slug(self):
        return "first-nations-rocket-competition"

    def get_code(self):
        if self.team.competition == "First Nations AISES":
            suffix = "AISES"
        else:
            suffix = "Tribal"
        return "FNL{}_{}".format(YEAR_2, suffix)

    def get_file_name(self):
        team_name = re.sub(r'[^a-zA-Z0-9]', '-', self.team.name)
        school_name = re.sub(
            r'[^a-zA-Z0-9]', '-',
            self.team.user.profile.get_registration().wsgc_affiliate.name
        )
        return u'{}_{}_{}_{}.{}'.format(
            self.get_code(), team_name, school_name,
            self.user.last_name, self.user.first_name
        )

    def get_media_release(self):
        return self.user.user_files.media_release

    def required_files(self):
        '''
        used when building a tarball of required files
        '''
        return ['media_release']

    @models.permalink
    def get_absolute_url(self):
        return ('application_update', [self.get_slug(), str(self.id)])


class HighAltitudeBalloon(BaseModel):

    class Meta:
        abstract = True

    # core
    letter_interest = models.FileField(
        "Letter of interest",
        upload_to = partial(upload_to_path, 'Letter_Interest'),
        validators=FILE_VALIDATORS,
        max_length=768,
        help_text="""
            Letter must include two faculty members' names, emails,
            and phone numbers, who can be contacted as references.
            [PDF format]
        """
    )
    commit = models.CharField(
        """
            Will you be able to commit 32-40 hours/week
            to this 10 week summer experience?
        """,
        max_length=4,
        null = True, blank = True,
        choices=BINARY_CHOICES,
    )
    cv = models.FileField(
        "Résumé",
        upload_to = partial(upload_to_path, 'CV'),
        validators=FILE_VALIDATORS,
        max_length=768,
        help_text="PDF format"
    )
    '''
    budget = models.FileField(
        upload_to = partial(upload_to_path, 'Budget'),
        validators=FILE_VALIDATORS,
        max_length=768,
        help_text="[PDF format]"
    )
    '''
    other_fellowship = models.CharField(
        "Do you currently hold another Federal fellowship or traineeship?",
        max_length=4,
        choices=BINARY_CHOICES,
    )
    other_fellowship_explain = models.CharField(
        """
            If yes, please provide the funding source and the
            funding expiration date.
        """,
        max_length=255,
        null = True, blank = True
    )

    def required_files(self):
        '''
        used when building a tarball of required files
        '''
        return ['letter_interest','cv']

    # timestamp methods are for UI level display
    def budget_timestamp(self):
        return self.get_file_timestamp("budget")

    @models.permalink
    def get_absolute_url(self):
        return ('application_update', [self.get_slug(), str(self.id)])


class HighAltitudeBalloonLaunch(HighAltitudeBalloon):
    """
    AKA: Elijah Balloon Launch
    """

    def __unicode__(self):
        return "High Altitude Balloon Launch"

    def get_application_type(self):
        return "High Altitude Balloon Launch"

    def get_slug(self):
        return "high-altitude-balloon-launch"

    def get_code(self):
        return "EBL{}".format(YEAR_2)

    class Meta:
        verbose_name_plural = "High altitude balloon launch"


class HighAltitudeBalloonPayload(HighAltitudeBalloon):
    """
    Elijah Balloon Payload
    """

    position = models.CharField(
        max_length=16,
        choices = (
            ('Team Lead','Team Lead'),
            ('Team Member','Team Member')
        ),
        help_text = '''
            Team Lead applicants must have participated in the program
            within the past 2 years.
        '''
    )

    def __unicode__(self):
        return "High Altitude Balloon Payload"

    def get_application_type(self):
        return "High Altitude Balloon Payload"

    def get_slug(self):
        return "high-altitude-balloon-payload"

    def get_code(self):
        return "EBP{}".format(YEAR_2)

    class Meta:
        verbose_name_plural = "High altitude balloon payload"


class Fellowship(BaseModel):

    class Meta:
        abstract = True

    # core
    anticipating_funding = models.CharField(
        "Are you anticipating other funding this year?",
        max_length=4,
        choices=BINARY_CHOICES,
        help_text="Grants/Scholarships/etc."
    )
    project_title = models.CharField(
        "Title of project", max_length=255
    )
    begin_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    funds_requested = models.IntegerField(help_text="In Dollars")
    funds_authorized = models.IntegerField(
        null = True, blank = True,
        help_text="In Dollars"
    )
    synopsis = models.TextField(
        help_text = '''
            Please include a short synopsis of your project
            (no more than 200 characters) outlining its purpose
            in terms understandable by the general reader.
            If your project is selected for funding, this
            wording will be used on our website.
        '''
    )
    nasa_mission_directorate = models.CharField(
        "NASA Mission directorate",
        max_length=128,
        choices=DIRECTORATE_CHOICES,
        help_text='''
            See NASA's
            <a href="http://www.nasa.gov/offices/education/missions/"
              target="_blank">
                Mission Directorates Education and Outreach
            </a> page for more information.
        '''
    )
    nasa_mission_directorate_other = models.CharField(
        "Other",
        max_length = 128,
        null = True, blank = True,
        help_text = '''
            If you have choosen "Other" in the field above,
            please identify the NASA Mission Directorate in which you are
            requesting funds to participate.
        '''
    )
    other_fellowship = models.CharField(
        "Do you currently hold another Federal fellowship or traineeship?",
        max_length=4,
        choices=BINARY_CHOICES,
    )
    other_fellowship_explain = models.CharField(
        """
            If yes, please provide the funding source and the
            funding expiration date.
        """,
        max_length=255,
        null = True, blank = True
    )
    proposal = models.FileField(
        upload_to = partial(upload_to_path, 'Proposal'),
        validators=FILE_VALIDATORS,
        max_length=768,
        help_text="PDF format"
    )
    cv = models.FileField(
        "Résumé",
        upload_to = partial(upload_to_path, 'CV'),
        validators=FILE_VALIDATORS,
        max_length=768,
        help_text="PDF format"
    )
    budget = models.FileField(
        upload_to = partial(upload_to_path, 'Budget'),
        validators=FILE_VALIDATORS,
        max_length=768,
        help_text="PDF format"
    )
    undergraduate_transcripts = models.FileField(
        upload_to = partial(upload_to_path, 'Undergraduate_Transcripts'),
        validators=FILE_VALIDATORS,
        max_length=768,
        help_text="PDF format"
    )
    graduate_transcripts = models.FileField(
        upload_to = partial(upload_to_path, 'Graduate_Transcripts'),
        validators=FILE_VALIDATORS,
        max_length=768,
        help_text="PDF format"
    )
    recommendation_1 = models.FileField(
        "Recommendation letter 1",
        upload_to = partial(upload_to_path, 'Recommendation_1'),
        validators=FILE_VALIDATORS,
        max_length=768,
        null=True,blank=True,
        help_text=mark_safe('''
            Recommendation letter is required for the application but may be
            emailed by Advisor directly to WSGC at
            <a href="mailto:spacegrant@carthage.edu">
                spacegrant@carthage.edu</a>.
            [PDF format]
        ''')
    )
    recommendation_2 = models.FileField(
        "Recommendation letter 2",
        upload_to = partial(upload_to_path, 'Recommendation_2'),
        validators=FILE_VALIDATORS,
        max_length=768,
        null = True, blank = True,
        help_text=mark_safe('''
            Recommendation letter is required for the application but may be
            emailed by Advisor directly to WSGC at
            <a href="mailto:spacegrant@carthage.edu">
                spacegrant@carthage.edu</a>.
            [PDF format]
        ''')
    )
    mentor_name = models.CharField(
        "Mentor's Name",
        max_length = 128
    )
    mentor_email = models.EmailField("Mentor's Email")
    signed_certification = models.BooleanField(
        """
        I certify that I am, will be, or have applied to be a
        full-time graduate student at one of the Wisconsin Space
        Grant Consortium colleges or universities during the award period
        covered in this application, and the information
        contained in this application is accurate to the best of my
        knowledge. I understand that, should I receive funding,
        some or all of this scholarship/fellowship may be taxable according
        to IRS regulations and that I am responsible for making sure all
        tax requirements are met.
        """,
        default=False
    )

    def __unicode__(self):
        return u"{}".format(self.project_title)

    def required_files(self):
        '''
        used when building a tarball of required files
        '''
        return [
            'proposal','cv','budget',
            'undergraduate_transcripts','graduate_transcripts',
            'recommendation_1', 'recommendation_2'
        ]

    # timestamp methods are for UI level display
    def budget_timestamp(self):
        return self.get_file_timestamp("budget")

    @models.permalink
    def get_absolute_url(self):
        return ('application_update', [self.get_slug(), str(self.id)])


class ClarkGraduateFellowship(Fellowship):

    def get_application_type(self):
        return "Dr. Laurel Salton Clark Memorial Research Fellowship"

    def get_slug(self):
        return "clark-graduate-fellowship"

    def get_code(self):
        return "LSC{}".format(YEAR_2)


class GraduateFellowship(Fellowship):
    """
    AKA: Research Fellowship Program
    """

    def get_application_type(self):
        return "WSGC Graduate &amp; Professional Research Fellowship"

    def get_slug(self):
        return "graduate-fellowship"

    def get_code(self):
        return "RFP{}".format(YEAR_2)


class UndergraduateResearch(BaseModel):

    # core
    project_title = models.CharField(
        "Title of project", max_length=255
    )
    funds_requested = models.IntegerField(help_text="In Dollars")
    funds_authorized = models.IntegerField(
        null = True, blank = True,
        help_text="In Dollars"
    )
    other_funding = models.CharField(
        "Are you seeking other WSGC funding for this project?",
        max_length=4,
        choices=BINARY_CHOICES,
    )
    other_funding_explain = models.CharField(
        "If yes, please explain",
        max_length=255,
        null = True, blank = True
    )
    other_fellowship = models.CharField(
        "Do you currently hold another Federal fellowship or traineeship?",
        max_length=4,
        choices=BINARY_CHOICES,
    )
    other_fellowship_explain = models.CharField(
        """
            If yes, please provide the funding source and the
            funding expiration date.
        """,
        max_length=255,
        null = True, blank = True
    )
    award_type = models.CharField(
        "Award",
        max_length = 128,
        choices = UNDERGRADUATE_RESEARCH_AWARD_TYPES
    )
    begin_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    synopsis = models.TextField(
        help_text = '''
            Please include a short synopsis of your project
            (no more than 200 characters) outlining its purpose
            in terms understandable by the general reader.
            If your project is selected for funding, this
            wording will be used on our website. [PDF format]
        '''
    )
    proposal = models.FileField(
        upload_to = partial(upload_to_path, 'Proposal'),
        validators=FILE_VALIDATORS,
        max_length=768,
        help_text="PDF format"
    )
    budget = models.FileField(
        upload_to = partial(upload_to_path, 'Budget'),
        validators=FILE_VALIDATORS,
        max_length=768,
        help_text="[PDF format]"
    )
    high_school_transcripts = models.FileField(
        upload_to = partial(upload_to_path, 'High_School_Transcripts'),
        validators=FILE_VALIDATORS,
        max_length=768,
        null = True, blank = True,
        help_text="High School Senior and Freshman students only. [PDF format]"
    )
    undergraduate_transcripts = models.FileField(
        upload_to = partial(upload_to_path, 'Undergraduate_Transcripts'),
        validators=FILE_VALIDATORS,
        max_length=768,
        help_text="PDF format"
    )
    wsgc_advisor_recommendation = models.FileField(
        "Faculty Research Advisor Recommendation Letter",
        upload_to = partial(upload_to_path, 'WSGC_Advisor_Recommendation'),
        validators=FILE_VALIDATORS,
        max_length=768,
        null = True, blank = True,
        help_text=mark_safe('''
            Recommendation letter is required for the application but may be
            emailed by Advisor directly to WSGC at
            <a href="mailto:spacegrant@carthage.edu">spacegrant@carthage.edu</a>.
            [PDF format]
        ''')
    )
    recommendation = models.FileField(
        """
            Additional Letter of Recommendation
            (faculty member or other professional reference)
        """,
        upload_to = partial(upload_to_path, 'Recommendation'),
        validators=FILE_VALIDATORS,
        max_length=768,
        null = True, blank = True,
        help_text=mark_safe('''
            Recommendation letter is required for the application but may be
            emailed by Advisor directly to WSGC at
            <a href="mailto:spacegrant@carthage.edu">
                spacegrant@carthage.edu</a>.
            [PDF format]
        ''')
    )
    mentor_name = models.CharField(
        "Mentor's Name",
        max_length = 128
    )
    mentor_email = models.EmailField("Mentor's Email")
    signed_certification = models.BooleanField(
        """
        I certify that I am, will be, or have applied to be a
        full-time graduate student at one of the Wisconsin Space
        Grant Consortium colleges or universities during the award period
        covered in this application, and the information
        contained in this application is accurate to the best of my
        knowledge. I understand that, should I receive funding,
        some or all of this scholarship/fellowship may be taxable according
        to IRS regulations and that I am responsible for making sure all
        tax requirements are met.
        """,
        default=False
    )

    def __unicode__(self):
        return u"{}".format(self.project_title)

    def get_application_type(self):
        return "Undergraduate Research Fellowship"

    def get_slug(self):
        return "undergraduate-research"

    def get_code(self):
        return "UGR{}".format(YEAR_2)

    def form(self):
        from djspace.application.forms import UndergraduateResearchForm
        return UndergraduateResearchForm

    def required_files(self):
        '''
        used when building a tarball of required files
        '''
        return [
            'proposal','budget','high_school_transcripts',
            'undergraduate_transcripts','wsgc_advisor_recommendation',
            'recommendation'
        ]

    # timestamp methods are for UI level display
    def budget_timestamp(self):
        return self.get_file_timestamp("budget")

    @models.permalink
    def get_absolute_url(self):
        return ('application_update', [self.get_slug(), str(self.id)])

    class Meta:
        verbose_name_plural = "Undergraduate Research"


class Scholarship(BaseModel):

    class Meta:
        abstract = True

    # core
    statement = models.FileField(
        upload_to = partial(upload_to_path, 'Statement'),
        validators=FILE_VALIDATORS,
        max_length=768,
        help_text=mark_safe('''Maximum two-page statement containing the following:
            <ol style="font-weight:bold;color:#000;list-style-type:upper-alpha;margin-left:25px;">
            <li>a clear and concise account of your reasons
            for seeking this scholarship</li>
            <li>evidence of previous interest and experience
            in space, aerospace, or space-related studies</li>
            <li>description of your present interest in the
            space sciences</li>
            <li>a description of the program of space-related
            studies you plan to pursue during the period of this
             award</li></ol> [PDF format]
        ''')
    )
    high_school_transcripts = models.FileField(
        upload_to = partial(upload_to_path, 'High_School_Transcripts'),
        validators=FILE_VALIDATORS,
        max_length=768,
        null = True, blank = True,
        help_text="First and second year students only. [PDF format]"
    )
    undergraduate_transcripts = models.FileField(
        upload_to = partial(upload_to_path, 'Undergraduate_Transcripts'),
        validators=FILE_VALIDATORS,
        max_length=768,
        help_text="PDF format"
    )
    wsgc_advisor_recommendation = models.FileField(
        "STEM Faculty/Advisor Recommendation Letter",
        upload_to = partial(upload_to_path, 'WSGC_Advisor_Recommendation'),
        validators=FILE_VALIDATORS,
        max_length=768,
        null = True, blank = True,
        help_text=mark_safe('''
            Recommendation letter is required for the application but may be
            emailed by Advisor directly to WSGC at
            <a href="mailto:spacegrant@carthage.edu">spacegrant@carthage.edu</a>.
            [PDF format]
        ''')
    )
    recommendation = models.FileField(
        """
            Additional Letter of Recommendation
            (faculty member or other professional reference)
        """,
        upload_to = partial(upload_to_path, 'Recommendation'),
        validators=FILE_VALIDATORS,
        max_length=768,
        null = True, blank = True,
        help_text=mark_safe('''
          Recommendation letter is required for the application but may be
          emailed by Advisor directly to WSGC at
          <a href="mailto:spacegrant@carthage.edu">spacegrant@carthage.edu</a>.
          [PDF format]
        ''')
    )
    academic_institution = models.CharField(
        "Application submitted for", max_length=128,
        choices=ACADEMIC_INSTITUTIONS
    )
    other_funding = models.CharField(
        "Are you seeking other WSGC funding for this project?",
        max_length=4,
        choices=BINARY_CHOICES,
    )
    other_funding_explain = models.CharField(
        "If yes, please explain",
        max_length=255,
        null = True, blank = True
    )
    other_fellowship = models.CharField(
        "Do you currently hold another Federal fellowship or traineeship?",
        max_length=4,
        choices=BINARY_CHOICES,
    )
    other_fellowship_explain = models.CharField(
        """
            If yes, please provide the funding source and the
            funding expiration date.
        """,
        max_length=255,
        null = True, blank = True
    )
    signed_certification = models.BooleanField(
        """
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
        default=False
    )

    def get_academic_institution(self):
        term = "FA"
        if "Spring" in self.academic_institution:
            term = "SP"
        return term

    def required_files(self):
        '''
        used when building a tarball of required files
        '''
        return [
            'statement','high_school_transcripts',
            'undergraduate_transcripts','wsgc_advisor_recommendation',
            'recommendation'
        ]


class UndergraduateScholarship(Scholarship):

    def __unicode__(self):
        return "Undergraduate Scholarship"

    def get_application_type(self):
        return "Undergraduate Scholarship"

    def get_slug(self):
        return "undergraduate-scholarship"

    def get_code(self):
        return "UGS{}_{}".format(
            YEAR_2, self.get_academic_institution()
        )

    @models.permalink
    def get_absolute_url(self):
        return ('application_update', [self.get_slug(), str(self.id)])


class StemBridgeScholarship(Scholarship):

    def __unicode__(self):
        return "STEM Bridge Scholarship"

    def get_application_type(self):
        return "STEM Bridge Scholarship"

    def get_slug(self):
        return "stem-bridge-scholarship"

    def get_code(self):
        return "SBS{}".format(YEAR_2)

    @models.permalink
    def get_absolute_url(self):
        return ('application_update', [self.get_slug(), str(self.id)])

    class Meta:
        verbose_name = "STEM Bridge Scholarship"
        verbose_name_plural = "STEM Bridge Scholarships"


class NasaCompetition(BaseModel):

    competition_type = models.CharField(
        """
            Type of NASA competition in which you are
            requesting funds to participate
        """,
        max_length = 128,
        choices = NASA_COMPETITION_TYPES
    )
    competition_type_other = models.CharField(
        "Other",
        max_length = 128,
        null = True, blank = True,
        help_text = '''
            If you have choosen "Other" in the field above,
            please identify the NASA Competition in which you are
            requesting funds to participate
        '''
    )
    facility_name = models.CharField(
        "NASA center",
        max_length = 128,
        choices = NASA_CENTER_CHOICES
    )
    facility_name_other = models.CharField(
        "Other",
        max_length = 128,
        null = True, blank = True,
        help_text = '''
            If you have choosen "Other" in the field above,
            please identify the competition location"
        '''
    )
    program_acceptance = models.CharField(
        "Has your team applied and been accepted into the program?",
        max_length = 4,
        choices = BINARY_CHOICES
    )
    award_type = models.CharField(
        "Award type",
        max_length = 128,
        choices = NASA_COMPETITION_AWARD_TYPES
    )
    funds_requested = models.IntegerField(help_text="In dollars")
    funds_authorized = models.IntegerField(
        null = True, blank = True,
        help_text = "In Dollars"
    )
    proposed_match = models.IntegerField(
        "Proposed match (25% mimimum)(in $)"
    )
    authorized_match = models.IntegerField(
        null = True, blank = True
    )
    source_match = models.CharField(
        "Source(s) of match", max_length = 255
    )
    begin_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    # files
    statement = models.FileField(
        upload_to = partial(upload_to_path, 'Statement'),
        validators=FILE_VALIDATORS,
        max_length = 768,
        help_text = "1 to 2 pages"
    )
    budget = models.FileField(
        upload_to = partial(upload_to_path, 'Budget'),
        validators=FILE_VALIDATORS,
        max_length = 768,
        help_text = "PDF format"
    )
    # finance officer
    finance_officer_name = models.CharField(
        "Name",
        max_length = 128
    )
    finance_officer_address = models.TextField("Address")
    finance_officer_email = models.EmailField("Email")
    finance_officer_phone = models.CharField(
        verbose_name = 'Phone number',
        max_length = 12,
        help_text = "Format: XXX-XXX-XXXX"
    )
    # grant officer
    grant_officer_name = models.CharField(
        "Name",
        max_length=128
    )
    grant_officer_address = models.TextField("Address")
    grant_officer_email = models.EmailField("Email")
    grant_officer_phone = models.CharField(
        verbose_name='Phone number',
        max_length=12,
        help_text="Format: XXX-XXX-XXXX"
    )
    # this is crazy and should be m2m but for now they do not
    # want to require members to be registered with the site
    member_1 = models.CharField(
        max_length=128,
        null = True, blank = True
    )
    member_2 = models.CharField(
        max_length=128,
        null = True, blank = True
    )
    member_3 = models.CharField(
        max_length=128,
        null = True, blank = True
    )
    member_4 = models.CharField(
        max_length=128,
        null = True, blank = True
    )
    member_5 = models.CharField(
        max_length=128,
        null = True, blank = True
    )
    member_6 = models.CharField(
        max_length=128,
        null = True, blank = True
    )
    member_7 = models.CharField(
        max_length=128,
        null = True, blank = True
    )
    member_8 = models.CharField(
        max_length=128,
        null = True, blank = True
    )
    member_9 = models.CharField(
        max_length=128,
        null = True, blank = True
    )
    member_10 = models.CharField(
        "Member 10",
        max_length=128,
        null = True, blank = True
    )
    team_lead = models.CharField(
        "Team Lead",
        max_length=128,
    )
    # approved files
    invoice = models.FileField(
        upload_to = partial(upload_to_path, 'Invoice'),
        validators=FILE_VALIDATORS,
        max_length=768,
        null=True, blank=True,
        help_text="PDF format"
    )
    intended_program_match = models.FileField(
        upload_to = partial(upload_to_path, 'Intended_Program_Match'),
        validators=FILE_VALIDATORS,
        max_length=768,
        null=True, blank=True,
        help_text="PDF format"
    )
    close_out_finance_document = models.FileField(
        upload_to = partial(upload_to_path, 'Closeout_Finance_Document'),
        validators=FILE_VALIDATORS,
        max_length=768,
        null=True, blank=True,
        help_text="PDF format"
    )

    class Meta:
        verbose_name_plural = "NASA Competitions"
        verbose_name = "NASA Competition"

    def __unicode__(self):
        return u"{}, {} [{}]".format(
            self.user.last_name, self.user.first_name, self.id
        )

    def get_application_type(self):
        return "NASA Competition"

    def get_slug(self):
        return "nasa-competition"

    def get_code(self):
        """
        OPP = Other Programs
        """

        if self.competition_type != "Other":
            program = re.sub(r'[^a-zA-Z0-9]', '-', self.competition_type)
        elif self.competition_type_other:
            program = re.sub(r'[^a-zA-Z0-9]', '-', self.competition_type_other)
        else:
            program = "other"
        return "OPP{}_{}_{}".format(
            YEAR_2, get_term(self.date_created), program
        )

    def required_files(self):
        '''
        used when building a tarball of required files
        '''
        return [ 'statement','budget']

    # timestamp methods are for UI level display
    def budget_timestamp(self):
        return self.get_file_timestamp("budget")

    @models.permalink
    def get_absolute_url(self):
        return ('application_update', [self.get_slug(), str(self.id)])


class IndustryInternship(BaseModel):

    award_type = models.CharField(
        "Award",
        max_length = 128,
        choices = INDUSTRY_AWARD_TYPES,
        help_text = """
            Select the opportunity to which the proposal is being submitted.
            <br><strong>NOTE</strong>:
            The $5000 award with optional match is only available to
            first time applicants.
        """
    )
    funds_requested = models.IntegerField(help_text="In dollars")
    funds_authorized = models.IntegerField(
        null = True, blank = True,
        help_text="In Dollars"
    )
    proposed_match = models.IntegerField(
        "Proposed match (1:1 mimimum)(in $)",
    )
    authorized_match = models.IntegerField(
        null = True, blank = True
    )
    source_match = models.CharField(
        "Source(s) of match", max_length=255
    )
    # Internship opportunity
    discipline = models.CharField(
        max_length = 128,
        choices = DISCIPLINES,
        null = True, blank = True,
        help_text = """
            Select the discipline within which the
            internship opportunity falls.
        """
    )
    discipline_other = models.CharField(
        max_length = 128,
        null = True, blank = True,
        help_text = '''
            If you have choosen "Other" in the field above,
            please provide the Discipline name here.
        '''
    )
    educational_background = models.TextField(
        # 500 character limit
        null = True, blank = True,
        help_text = """
            Provide additional information related to the required educational
            background for the internship opportunity.
        """
    )
    # Intern Supervisor
    intern_supervisor_name = models.CharField(
        "Name",
        max_length = 128,
        null = True, blank = True
    )
    intern_supervisor_job_title = models.CharField(
        "Job title",
        max_length = 128,
        null = True, blank = True
    )
    intern_supervisor_cv = models.FileField(
        "Brief Résumé",
        upload_to = partial(upload_to_path, 'Intern_Supervisor_CV'),
        validators=FILE_VALIDATORS,
        max_length = 768,
        null = True, blank = True,
        help_text = "PDF format"
    )
    # Work description
    objective_technical_approach = models.TextField(
        "Objective and Technical Approach",
        # 2500 character limit
        null = True, blank = True
    )
    background = models.TextField(
        # 2500 character limit
        null = True, blank = True
    )
    background_photo = models.ImageField(
        "Photo",
        upload_to = partial(upload_to_path, 'Background_Photo'),
        validators=PHOTO_VALIDATORS,
        max_length = 768,
        null = True, blank = True,
        help_text = "JPEG only"
    )
    # WorkPlanTask model has a foreign key that references
    # an instance of this model. we can obtain all tasks for
    # an instance with the related name "work_plan_tasks"
    task_schedule = models.FileField(
        upload_to = partial(upload_to_path, 'Task_Schedule'),
        max_length = 768,
        null = True, blank = True,
        help_text = """
            You must include milestones and the file format must be:
            Excel, Word, or Project.
        """
    )
    wsgc_goal = models.TextField(
        # 500 character limit
        null = True, blank = True,
        help_text = '''
            How does this internship opportunity address the WSGC goal of
            "Career placements within the aerospace industry in Wisconsin".
        '''
    )
    nasa_mission_relationship = models.TextField(
        "NASA Mission directorate",
        # 1250 character limit
        null = True, blank = True,
        help_text = '''
            How does this internship opportunity relate to NASAs mission?
            Can the work be related to a specific NASA center?
        '''
    )
    intern_biography = models.TextField(
        # 1250 character limit
        null = True, blank = True,
        help_text = '''
            If a candidate student has been identified, provide a brief
            biosketch of the company intern and his or her career goals,
            if available. Though this information is not part of the proposal
            evaluation, it is important to assure that all internships are
            filled with students qualified to be funded through the WSGC.
        '''
    )
    budget = models.FileField(
        upload_to = partial(upload_to_path, 'Budget'),
        validators=FILE_VALIDATORS,
        max_length = 768,
        help_text = "PDF format"
    )
    # approved files
    invoice = models.FileField(
        upload_to = partial(upload_to_path, 'Invoice'),
        validators=FILE_VALIDATORS,
        max_length=768,
        null=True, blank=True,
        help_text="PDF format"
    )
    intended_program_match = models.FileField(
        upload_to = partial(upload_to_path, 'Intended_Program_Match'),
        validators=FILE_VALIDATORS,
        max_length=768,
        null=True, blank=True,
        help_text="PDF format"
    )
    close_out_finance_document = models.FileField(
        upload_to = partial(upload_to_path, 'Closeout_Finance_Document'),
        validators=FILE_VALIDATORS,
        max_length=768,
        null=True, blank=True,
        help_text="PDF format"
    )

    def __unicode__(self):
        return u"{}, {} [{}]".format(
            self.user.last_name, self.user.first_name, self.id
        )

    def get_application_type(self):
        return "Industry Internship"

    def get_slug(self):
        return "industry-internship"

    def get_code(self):
        return "IIP{}".format(YEAR_2)

    def required_files(self):
        '''
        used when building a tarball of required files
        '''
        return ['intern_supervisor_cv','task_schedule','budget']

    # timestamp methods are for UI level display
    def budget_timestamp(self):
        return self.get_file_timestamp("budget")

    @models.permalink
    def get_absolute_url(self):
        return ('application_update', [self.get_slug(), str(self.id)])


class ProfessionalProgramStudent(BaseModel):

    program = models.CharField(
        "Program Name",
        max_length = 128,
        choices=STUDENT_PROFESSIONAL_PROGRAMS,
        help_text = '''
            I, as a student, have been selected to participate
            in the above program
        '''
    )
    budget = models.FileField(
        upload_to = partial(upload_to_path, 'Budget'),
        validators=FILE_VALIDATORS,
        max_length=768,
        null=True, blank=True,
        help_text="[PDF format]"
    )
    mentor = models.ForeignKey(
        User,
        related_name='professional_program_student'
    )
    AerospaceOutreach = models.ForeignKey(
        AerospaceOutreach,
        related_name='aerospace_outreach_student',
        null=True, blank=True
    )
    HigherEducationInitiatives  = models.ForeignKey(
        HigherEducationInitiatives,
        related_name='higher_education_initiatives_student',
        null=True, blank=True
    )
    IndustryInternship = models.ForeignKey(
        IndustryInternship,
        related_name='industry_internship_student',
        null=True, blank=True
    )
    NasaCompetition = models.ForeignKey(
        NasaCompetition,
        related_name='nasa_competition_student',
        null=True, blank=True
    )
    ResearchInfrastructure = models.ForeignKey(
        ResearchInfrastructure,
        related_name='research_infrastructure_student',
        null=True, blank=True
    )
    SpecialInitiatives = models.ForeignKey(
        SpecialInitiatives,
        related_name='special_initiatives_student',
        null=True, blank=True
    )

    class Meta:
        verbose_name_plural = "Professional Program Student Participation"

    def __unicode__(self):
        return "Professional Program Student"

    @models.permalink
    def get_absolute_url(self):
        return ('application_update', [self.get_slug(), str(self.id)])

    def get_application_type(self):
        return "Professional Program Student"

    def get_slug(self):
        return "professional-program-student"

    def program_application(self):
        obj = None
        if self.AerospaceOutreach:
            obj = self.AerospaceOutreach
        elif self.HigherEducationInitiatives:
            obj = self.HigherEducationInitiatives
        elif self.IndustryInternship:
            obj = self.IndustryInternship
        elif self.NasaCompetition:
            obj = self.NasaCompetition
        elif self.ResearchInfrastructure:
            obj = self.ResearchInfrastructure
        elif self.SpecialInitiatives:
            obj = self.SpecialInitiatives
        return obj

    def program_application_link(self):
        app = self.program_application()
        link = None
        if app:
            # two programs do not have a title so we use app name instead
            try:
                title = app.project_title
            except:
                #title = app.__class__.__name__
                title = self.program
            url = reverse(
                'application_print',
                kwargs={'application_type':app.get_slug(),'aid': app.id},
            )
            link = u'<a href="{}">{}</a>'.format(url, title)
        return link

    def get_code(self):
        return "PPS{}_{}".format(YEAR_2, self.program)

    def media_release(self):
        return self.user.user_files.media_release

    def biography(self):
        return self.user.user_files.biography

    def mugshot(self):
        return self.user.user_files.mugshot

    def required_files(self):
        '''
        used when building a tarball of required files
        '''
        return ['budget',]

    # timestamp methods are for UI level display
    def budget_timestamp(self):
        return self.get_file_timestamp("budget")


class WorkPlanTask(models.Model):
    industry_internship = models.ForeignKey(
        IndustryInternship,
        related_name="work_plan_tasks",
    )
    title = models.CharField(
        max_length = 128,
        null = True, blank = True
    )
    description = models.TextField(
        null = True, blank = True
    )
    hours_percent = models.CharField(
        max_length = 32,
        null = True, blank = True
    )
    expected_outcome = models.TextField(
        null = True, blank = True
    )

    def __unicode__(self):
        return u"{}".format(self.title)
