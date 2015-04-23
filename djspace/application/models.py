# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe

from djspace.core.models import BaseModel

from djtools.fields import BINARY_CHOICES, SALUTATION_TITLES, STATE_CHOICES
from djtools.fields import GENDER_CHOICES
from djtools.fields.validators import MimetypeValidator

from uuid import uuid4

import os

GRAVITY_TRAVEL = (
    ('gravity','Reduced Gravity'),
    ('travel','Student Travel')
)

ROLE = (
    ('Faculty Advisor','Faculty Advisor'),
    ('Team leader','Team Leader'),
)

TIME_FRAME = (
    ('Summer','Summer'),
    ('Summer and fall','Summer and fall'),
    ('Fall','Fall'),
    ('Spring','Spring'),
    ('Summer, fall, and spring','Summer, fall, and spring'),
    ('Fall and spring','Fall and spring')
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

    # core
    project_title = models.CharField(
        "Title of project", max_length=255
    )
    funds_requested = models.IntegerField(help_text="In Dollars")
    funds_authorized = models.IntegerField(
        null=True,blank=True,
        help_text="In Dollars"
    )
    proposed_match = models.IntegerField(
        "Proposed match (1:1 mimimum)(in $)",
    )
    source_match = models.CharField(
        "Source(s) of match", max_length=255
    )
    time_frame = models.CharField(
        "Time frame that best suits your project",
        max_length=128,
        choices=TIME_FRAME
    )
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
        help_text="PDF format."
    )

    class Meta:
        abstract = True


class HigherEducationInitiatives(EducationInitiatives):

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

    def __unicode__(self):
        return "Special Initiatives"

    def get_application_type(self):
        return "Special Initiatives"

    def get_slug(self):
        return "aerospace-outreach"

    @models.permalink
    def get_absolute_url(self):
        return ('application_update', [self.get_slug(), str(self.id)])

    class Meta:
        verbose_name_plural = "Special Initiatives"


class FirstNationsLaunchCompetition(BaseModel):

    # core
    team_name = models.CharField(
        max_length=255
    )
    role = models.CharField(
        "Your Role",
        max_length=128,
        choices=ROLE
    )
    proposal = models.FileField(
        "Proposal",
        upload_to=upload_to_path,
        validators=[MimetypeValidator('application/pdf')],
        max_length=768,
        help_text="""
            PDF format.
        """
    )

    def __unicode__(self):
        return "First Nations Launch Competition"

    def get_application_type(self):
        return "First Nations Launch Competition"

    def get_slug(self):
        return "first-nations-launch-competition"

    @models.permalink
    def get_absolute_url(self):
        return ('application_update', [self.get_slug(), str(self.id)])


class HighAltitudeBalloonLaunch(BaseModel):

    # core
    letter_interest = models.FileField(
        "Letter of interest",
        upload_to=upload_to_path,
        validators=[MimetypeValidator('application/pdf')],
        max_length=768,
        help_text="""
            Letter must include two faculty members' names, emails,
            and phone numbers, who can be contacted as references.
            PDF format.
        """
    )
    cv = models.FileField(
        "Résumé",
        upload_to=upload_to_path,
        validators=[MimetypeValidator('application/pdf')],
        max_length=768,
        help_text="PDF format."
    )

    def __unicode__(self):
        return "High Altitude Balloon Launch"

    def get_application_type(self):
        return "High Altitude Balloon Launch"

    def get_slug(self):
        return "high-altitude-balloon-launch"

    @models.permalink
    def get_absolute_url(self):
        return ('application_update', [self.get_slug(), str(self.id)])

    class Meta:
        verbose_name_plural = "High altitude balloon launch"


class HighAltitudeBalloonPayload(HighAltitudeBalloonLaunch):

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
    time_frame = models.CharField(
        "Time frame that best suits your project",
        max_length=128,
        choices=TIME_FRAME
    )
    funds_requested = models.IntegerField(help_text="In Dollars")
    funds_authorized = models.IntegerField(
        null=True,blank=True,
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
    proposal = models.FileField(
        upload_to=upload_to_path,
        validators=[MimetypeValidator('application/pdf')],
        max_length=768,
        help_text="PDF format."
    )
    cv = models.FileField(
        "Résumé",
        upload_to=upload_to_path,
        validators=[MimetypeValidator('application/pdf')],
        max_length=768,
        help_text="PDF format."
    )
    budget = models.FileField(
        upload_to=upload_to_path,
        validators=[MimetypeValidator('application/pdf')],
        max_length=768,
        help_text="PDF format."
    )
    undergraduate_transcripts = models.FileField(
        upload_to=upload_to_path,
        validators=[MimetypeValidator('application/pdf')],
        max_length=768,
        help_text="PDF format."
    )
    graduate_transcripts = models.FileField(
        upload_to=upload_to_path,
        validators=[MimetypeValidator('application/pdf')],
        max_length=768,
        help_text="PDF format."
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
            <a href="mailto:spacegrant@carthage.edu">spacegrant@carthage.edu</a>.
            PDF format.
        ''')
    )
    recommendation_2 = models.FileField(
        "Recommendation letter 2",
        upload_to=upload_to_path,
        validators=[MimetypeValidator('application/pdf')],
        max_length=768,
        null=True,blank=True,
        help_text=mark_safe('''
            Recommendation letter is required for the application but may be
            emailed by Advisor directly to WSGC at
            <a href="mailto:spacegrant@carthage.edu">spacegrant@carthage.edu</a>.
            PDF format.
        ''')
    )

    def __unicode__(self):
        return self.project_title

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
        null=True,blank=True,
        help_text="In Dollars"
    )
    time_frame = models.CharField(
        "Time frame that best suits your project",
        max_length=128,
        choices=TIME_FRAME
    )
    synopsis = models.TextField(
        help_text = '''
            Please include a short synopsis of your project
            (no more than 200 characters) outlining its purpose
            in terms understandable by the general reader.
            If your project is selected for funding, this
            wording will be used on our website. PDF format.
        '''
    )
    proposal = models.FileField(
        upload_to=upload_to_path,
        validators=[MimetypeValidator('application/pdf')],
        max_length=768,
        help_text="PDF format."
    )
    high_school_transcripts = models.FileField(
        upload_to=upload_to_path,
        validators=[MimetypeValidator('application/pdf')],
        max_length=768,
        null=True,blank=True,
        help_text="First and second year students only. PDF format."
    )
    undergraduate_transcripts = models.FileField(
        upload_to=upload_to_path,
        validators=[MimetypeValidator('application/pdf')],
        max_length=768,
        help_text="PDF format."
    )
    wsgc_advisor_recommendation = models.FileField(
        "Faculty Research Advisor Recommendation Letter",
        upload_to=upload_to_path,
        validators=[MimetypeValidator('application/pdf')],
        max_length=768,
        null=True,blank=True,
        help_text=mark_safe('''
            Recommendation letter is required for the application but may be
            emailed by Advisor directly to WSGC at
            <a href="mailto:spacegrant@carthage.edu">spacegrant@carthage.edu</a>.
            PDF format.
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
        null=True,blank=True,
        help_text=mark_safe('''
            Recommendation letter is required for the application but may be
            emailed by Advisor directly to WSGC at
            <a href="mailto:spacegrant@carthage.edu">spacegrant@carthage.edu</a>.
            PDF format.
        ''')
    )

    def __unicode__(self):
        return self.project_title

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
             award.</li></ol> PDF format.
        ''')
    )
    high_school_transcripts = models.FileField(
        upload_to=upload_to_path,
        validators=[MimetypeValidator('application/pdf')],
        max_length=768,
        null=True,blank=True,
        help_text="First and second year students only. PDF format."
    )
    undergraduate_transcripts = models.FileField(
        upload_to=upload_to_path,
        validators=[MimetypeValidator('application/pdf')],
        max_length=768,
        help_text="PDF format."
    )
    wsgc_advisor_recommendation = models.FileField(
        "Faculty Research Advisor Recommendation Letter",
        upload_to=upload_to_path,
        validators=[MimetypeValidator('application/pdf')],
        max_length=768,
        null=True,blank=True,
        help_text=mark_safe('''
            Recommendation letter is required for the application but may be
            emailed by Advisor directly to WSGC at
            <a href="mailto:spacegrant@carthage.edu">spacegrant@carthage.edu</a>.
            PDF format.
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
        null=True,blank=True,
        help_text=mark_safe('''
            Recommendation letter is required for the application but may be
            emailed by Advisor directly to WSGC at
            <a href="mailto:spacegrant@carthage.edu">spacegrant@carthage.edu</a>.
            PDF format.
        ''')
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

