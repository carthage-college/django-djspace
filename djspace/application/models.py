# -*- coding: utf-8 -*-
from django.db import models
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from django.db.models.signals import pre_delete

from djspace.core.models import BaseModel
from djspace.registration.choices import WSGC_SCHOOL

from djtools.fields import BINARY_CHOICES, SALUTATION_TITLES, STATE_CHOICES
from djtools.fields import GENDER_CHOICES
from djtools.fields.validators import MimetypeValidator

from uuid import uuid4

WSGC_SCHOOL_OTHER = WSGC_SCHOOL + (('Other','Other'),)

import os

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
FIRST_NATIONS_ROCKET_COMPETITIONS = (
    ('Tribal Challenge','Tribal Challenge'),
    ('AISES Challenge','AISES Challenge'),
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
        'STEM Bridge (Spring)','STEM Bridge (Spring)'
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
ROCKET_COMPETITIONS = (
    ("Collegiate Rocket Competition", "Collegiate Rocket Competition"),
    ("First Nations AISES", "First Nations AISES"),
    ("First Nations Tribal", "First Nations Tribal"),
    (
        "Midwest High Powered Rocket Competition",
        "Midwest High Powered Rocket Competition"
    )
)


def upload_to_path(self, filename):
    """
    Generates the path as a string for file field.
    """
    ext = filename.split('.')[-1]
    # set filename as random string
    filename = '{}.{}'.format(uuid4().hex, ext)
    ts = self.date_created.strftime("%Y%m%d%H%M%S%f")
    path = "files/applications/{}/{}/{}/".format(
        self.get_slug(), self.user.id, ts
    )
    return os.path.join(path, filename)


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
    begin_date = models.DateField()
    end_date = models.DateField()
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
        upload_to=upload_to_path,
        validators=[MimetypeValidator('application/pdf')],
        max_length=768,
        help_text="PDF format"
    )
    finance_officer_name = models.CharField(
        "Name",
        max_length=128
    )
    finance_officer_address = models.TextField("Address")
    finance_officer_email = models.EmailField("Email")
    finance_officer_phone = models.CharField(
        verbose_name='Phone number',
        max_length=12,
        help_text="Format: XXX-XXX-XXXX"
    )


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
        return "Higher Education Initiatives"

    def get_application_type(self):
        return "Higher Education Initiatives"

    def get_slug(self):
        return "higher-education-initiatives"

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
        max_length=128,
        choices=DIRECTORATE_CHOICES,
        help_text='''
            See NASA's
            <a href="https://www.nasa.gov/offices/education/missions/">
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
        return "Research Infrastructure"

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
        max_length=128,
        choices=DIRECTORATE_CHOICES,
        help_text='''
            See NASA's
            <a href="https://www.nasa.gov/offices/education/missions/">
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
        return "Aerospace Outreach"

    def get_application_type(self):
        return "Aerospace Outreach"

    def get_slug(self):
        return "aerospace-outreach"

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
        max_length=128,
        choices=DIRECTORATE_CHOICES,
        help_text='''
            See NASA's
            <a href="https://www.nasa.gov/offices/education/missions/">
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
        return "Special Initiatives"

    def get_application_type(self):
        return "Special Initiatives"

    def get_slug(self):
        return "special-initiatives"

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
    academic_institution_name = models.CharField(
        "Academic institution",
        choices=WSGC_SCHOOL_OTHER,
        max_length=128,
    )
    academic_institution_other = models.CharField(
        "Other",
        max_length=128,
        null = True, blank = True,
        help_text="""
            If your academic institution does not appear in the list above,
            please provide it here.
        """
    )
    leader = models.ForeignKey(
        User,
        verbose_name="Team lead",
        related_name="rocket_launch_team_leader",
    )
    industry_mentor_name = models.CharField(
        max_length=128,
        null = True, blank = True
    )
    industry_mentor_email = models.EmailField(
        max_length=75,
        null = True, blank = True
    )
    intent_compete = models.TextField(
        "Notification of Intent to Compete"
    )
    wsgc_acknowledgement = models.FileField(
        "WSGC institutional representative acknowledgement",
        upload_to=upload_to_path,
        validators=[MimetypeValidator('application/pdf')],
        max_length=768,
        null = True, blank = True,
        help_text="""
            [PDF format]<br>
            NOTE: Only required for the Collegiate Rocket Competition<br>
            and the Midwest High-Powered Rocket Competition.
        """
    )
    budget = models.FileField(
        upload_to=upload_to_path,
        validators=[MimetypeValidator('application/pdf')],
        max_length=768,
        null = True, blank = True,
        help_text="""
            Rocket supplies and travel. [PDF format]<br>
            NOTE: Only required for the
            Midwest High-Powered Rocket Competition.
        """
    )
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
    # meta
    competition = models.CharField(
        choices =  ROCKET_COMPETITIONS,
        max_length=128
    )

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

    def get_team_members(self):
        team = None
        if self.competition == "Collegiate Rocket Competition":
            team = self.collegiate_rocket_competition
        elif self.competition == "Midwest High Powered Rocket Competition":
            team = self.midwest_high_powered_rocket_competition
        elif "First Nations" in self.competition:
            team = self.first_nations_rocket_competition
        return team

    @models.permalink
    def get_absolute_url(self):
        return ('application_update', [self.get_slug(), str(self.id)])


class MidwestHighPoweredRocketCompetition(BaseModel):

    # core
    team = models.ForeignKey(
        RocketLaunchTeam,
        related_name="midwest_high_powered_rocket_competition"
    )
    cv = models.FileField(
        "Résumé",
        upload_to=upload_to_path,
        validators=[MimetypeValidator('application/pdf')],
        max_length=768,
        help_text="PDF format"
    )
    prior_experience = models.TextField(
        "Prior Rocket Experience"
    )

    def __unicode__(self):
        return "Midwest High-Powered Rocket Competition"

    def get_application_type(self):
        return "Midwest High-Powered Rocket Competition"

    def get_slug(self):
        return "midwest-high-powered-rocket-competition"

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
        upload_to=upload_to_path,
        validators=[MimetypeValidator('application/pdf')],
        max_length=768,
        help_text="PDF format"
    )

    def __unicode__(self):
        return "Collegiate Rocket Competition"

    def get_application_type(self):
        return "Collegiate Rocket Competition"

    def get_slug(self):
        return "collegiate-rocket-competition"

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
    media_release = models.FileField(
        upload_to=upload_to_path,
        validators=[MimetypeValidator('application/pdf')],
        max_length=768,
        help_text="PDF format"
    )

    def __unicode__(self):
        return "First Nations Rocket Competition"

    def get_application_type(self):
        return "First Nations Rocket Competition"

    def get_slug(self):
        return "first-nations-rocket-competition"

    def team_name(self):
        return self.team.name

    @models.permalink
    def get_absolute_url(self):
        return ('application_update', [self.get_slug(), str(self.id)])


class HighAltitudeBalloon(BaseModel):

    class Meta:
        abstract = True

    # core
    letter_interest = models.FileField(
        "Letter of interest",
        upload_to=upload_to_path,
        validators=[MimetypeValidator('application/pdf')],
        max_length=768,
        help_text="""
            Letter must include two faculty members' names, emails,
            and phone numbers, who can be contacted as references.
            [PDF format]
        """
    )
    cv = models.FileField(
        "Résumé",
        upload_to=upload_to_path,
        validators=[MimetypeValidator('application/pdf')],
        max_length=768,
        help_text="PDF format"
    )

    @models.permalink
    def get_absolute_url(self):
        return ('application_update', [self.get_slug(), str(self.id)])


class HighAltitudeBalloonLaunch(HighAltitudeBalloon):

    def __unicode__(self):
        return "High Altitude Balloon Launch"

    def get_application_type(self):
        return "High Altitude Balloon Launch"

    def get_slug(self):
        return "high-altitude-balloon-launch"

    class Meta:
        verbose_name_plural = "High altitude balloon launch"

class HighAltitudeBalloonPayload(HighAltitudeBalloon):

    def __unicode__(self):
        return "High Altitude Balloon Payload"

    def get_application_type(self):
        return "High Altitude Balloon Payload"

    def get_slug(self):
        return "high-altitude-balloon-payload"

    class Meta:
        verbose_name_plural = "High altitude balloon payload"


class Fellowship(BaseModel):

    class Meta:
        abstract = True

    # core
    signed_certification = models.FileField(
        upload_to=upload_to_path,
        validators=[MimetypeValidator('application/pdf')],
        max_length=768,
        help_text=mark_safe('''
            Before beginning the application process,
            please print, obtain signatures, and scan the<br>
            <a href="/live/files/1808-pdf" target="_blank">
            signed certification document
            </a>.
        ''')
    )
    anticipating_funding = models.CharField(
        "Are you anticipating other funding this year?",
        max_length=4,
        choices=BINARY_CHOICES,
        help_text="Grants/Scholarships/etc."
    )
    project_title = models.CharField(
        "Title of project", max_length=255
    )
    '''
    time_frame = models.CharField(
        "Time frame that best suits your project",
        max_length=128,
        choices=TIME_FRAME
    )
    '''
    begin_date = models.DateField()
    end_date = models.DateField()
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
        max_length=128,
        choices=DIRECTORATE_CHOICES,
        help_text='''
            See NASA's
            <a href="http://www.nasa.gov/offices/education/missions/">
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
    proposal = models.FileField(
        upload_to=upload_to_path,
        validators=[MimetypeValidator('application/pdf')],
        max_length=768,
        help_text="PDF format"
    )
    cv = models.FileField(
        "Résumé",
        upload_to=upload_to_path,
        validators=[MimetypeValidator('application/pdf')],
        max_length=768,
        help_text="PDF format"
    )
    budget = models.FileField(
        upload_to=upload_to_path,
        validators=[MimetypeValidator('application/pdf')],
        max_length=768,
        help_text="PDF format"
    )
    undergraduate_transcripts = models.FileField(
        upload_to=upload_to_path,
        validators=[MimetypeValidator('application/pdf')],
        max_length=768,
        help_text="PDF format"
    )
    graduate_transcripts = models.FileField(
        upload_to=upload_to_path,
        validators=[MimetypeValidator('application/pdf')],
        max_length=768,
        help_text="PDF format"
    )
    recommendation_1 = models.FileField(
        "Recommendation letter 1",
        upload_to=upload_to_path,
        validators=[MimetypeValidator('application/pdf')],
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
        upload_to=upload_to_path,
        validators=[MimetypeValidator('application/pdf')],
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

    def __unicode__(self):
        return u"{}".format(self.project_title)

    @models.permalink
    def get_absolute_url(self):
        return ('application_update', [self.get_slug(), str(self.id)])


class ClarkGraduateFellowship(Fellowship):

    def get_application_type(self):
        return "Dr. Laurel Salton Clark Memorial Research Fellowship"

    def get_slug(self):
        return "clark-graduate-fellowship"


class GraduateFellowship(Fellowship):

    def get_application_type(self):
        return "WSGC Graduate &amp; Professional Research Fellowship"

    def get_slug(self):
        return "graduate-fellowship"


class UndergraduateResearch(BaseModel):

    # core
    signed_certification = models.FileField(
        upload_to=upload_to_path,
        validators=[MimetypeValidator('application/pdf')],
        max_length=768,
        help_text=mark_safe('''
            Before beginning the application process,
            please print, obtain signatures, and scan the<br>
            <a href="/live/files/1827-pdf" target="_blank">
            signed certification document
            </a>
        ''')
    )
    project_title = models.CharField(
        "Title of project", max_length=255
    )
    funds_requested = models.IntegerField(help_text="In Dollars")
    funds_authorized = models.IntegerField(
        null = True, blank = True,
        help_text="In Dollars"
    )
    award_type = models.CharField(
        "Award",
        max_length = 128,
        choices = UNDERGRADUATE_RESEARCH_AWARD_TYPES
    )
    '''
    time_frame = models.CharField(
        "Time frame that best suits your project",
        max_length=128,
        choices=TIME_FRAME
    )
    '''
    begin_date = models.DateField()
    end_date = models.DateField()
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
        upload_to=upload_to_path,
        validators=[MimetypeValidator('application/pdf')],
        max_length=768,
        help_text="PDF format"
    )
    high_school_transcripts = models.FileField(
        upload_to=upload_to_path,
        validators=[MimetypeValidator('application/pdf')],
        max_length=768,
        null = True, blank = True,
        help_text="First and second year students only. [PDF format]"
    )
    undergraduate_transcripts = models.FileField(
        upload_to=upload_to_path,
        validators=[MimetypeValidator('application/pdf')],
        max_length=768,
        help_text="PDF format"
    )
    wsgc_advisor_recommendation = models.FileField(
        "Faculty Research Advisor Recommendation Letter",
        upload_to=upload_to_path,
        validators=[MimetypeValidator('application/pdf')],
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
        upload_to=upload_to_path,
        validators=[MimetypeValidator('application/pdf')],
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

    def __unicode__(self):
        return u"{}".format(self.project_title)

    def get_application_type(self):
        return "Undergraduate Research Fellowship"

    def get_slug(self):
        return "undergraduate-research"

    @models.permalink
    def get_absolute_url(self):
        return ('application_update', [self.get_slug(), str(self.id)])

    class Meta:
        verbose_name_plural = "Undergraduate Research"

class UndergraduateScholarship(BaseModel):

    # core
    signed_certification = models.FileField(
        upload_to=upload_to_path,
        validators=[MimetypeValidator('application/pdf')],
        max_length=768,
        help_text=mark_safe('''
            Before beginning the application process,
            please print, obtain signatures, and scan the<br>
            <a href="/live/files/1827-pdf" target="_blank">
            signed certification document
            </a>
        ''')
    )
    statement = models.FileField(
        upload_to=upload_to_path,
        validators=[MimetypeValidator('application/pdf')],
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
             award.</li></ol> [PDF format]
        ''')
    )
    high_school_transcripts = models.FileField(
        upload_to=upload_to_path,
        validators=[MimetypeValidator('application/pdf')],
        max_length=768,
        null = True, blank = True,
        help_text="First and second year students only. [PDF format]"
    )
    undergraduate_transcripts = models.FileField(
        upload_to=upload_to_path,
        validators=[MimetypeValidator('application/pdf')],
        max_length=768,
        help_text="PDF format"
    )
    wsgc_advisor_recommendation = models.FileField(
        "STEM Faculty/Advisor Recommendation Letter",
        upload_to=upload_to_path,
        validators=[MimetypeValidator('application/pdf')],
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
        upload_to=upload_to_path,
        validators=[MimetypeValidator('application/pdf')],
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

    def __unicode__(self):
        return "Undergraduate Scholarship"

    def get_application_type(self):
        return "Undergraduate Scholarship"

    def get_slug(self):
        return "undergraduate-scholarship"

    @models.permalink
    def get_absolute_url(self):
        return ('application_update', [self.get_slug(), str(self.id)])


class NasaCompetition(BaseModel):

    competition_type = models.CharField(
        "Type of NASA competition",
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
    end_date = models.DateField()
    statement = models.FileField(
        upload_to = upload_to_path,
        validators = [MimetypeValidator('application/pdf')],
        max_length = 768,
        help_text = "1 to 2 pages"
    )
    budget = models.FileField(
        upload_to = upload_to_path,
        validators = [MimetypeValidator('application/pdf')],
        max_length = 768,
        help_text = "PDF format"
    )
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

    def __unicode__(self):
        return "NASA Competition"

    def get_application_type(self):
        return "NASA Competition"

    def get_slug(self):
        return "nasa-competition"

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
        upload_to = upload_to_path,
        validators = [MimetypeValidator('application/pdf')],
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
        upload_to = upload_to_path,
        validators = [MimetypeValidator('image/jpeg')],
        max_length = 768,
        null = True, blank = True,
        help_text = "JPEG only"
    )
    # WorkPlanTask model has a foreign key the references
    # an instance of this model. we can obtain all tasks for
    # an instance with the related name "work_plan_tasks"
    task_schedule = models.FileField(
        upload_to = upload_to_path,
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
        upload_to = upload_to_path,
        validators = [MimetypeValidator('application/pdf')],
        max_length = 768,
        null = True, blank = True,
        help_text = "PDF format"
    )

    def __unicode__(self):
        return u"{}, {}".format(self.user.last_name, self.user.first_name)

    def get_application_type(self):
        return "Industry Internship"

    def get_slug(self):
        return "industry-internship"

    @models.permalink
    def get_absolute_url(self):
        return ('application_update', [self.get_slug(), str(self.id)])


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

