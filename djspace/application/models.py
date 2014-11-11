# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe

from djspace.registration.validators import MimetypeValidator
from djtools.fields import BINARY_CHOICES, SALUTATION_TITLES, STATE_CHOICES
from djtools.fields import GENDER_CHOICES

GRAVITY_TRAVEL = (
    ('gravity','Reduced Gravity'),
    ('travel','Student Travel')
)

TITLE = (
    ('advisor','Faculty Advisor'),
    ('leader','Team Lead'),
    ('member','Member')
)

TIME_FRAME = (
    ('Summer','Summer'),
    ('Summer and fall','Summer and fall'),
    ('Fall','Fall'),
    ('Spring','Spring'),
    ('Summer, fall, and spring','Summer, fall, and spring'),
    ('Fall and spring','Fall and spring')
)

class HighAltitudeBalloonLaunch(models.Model):

    # meta
    user = models.ForeignKey(User)
    status = models.BooleanField(default=False)
    updated_by = models.ForeignKey(
        User, verbose_name="Updated by",
        related_name="habl_updated_by",
        editable=False
    )
    date_created = models.DateTimeField(
        "Date Created", auto_now_add=True
    )
    date_updated = models.DateTimeField(
        "Date Updated", auto_now=True
    )
    # core
    letter_interest = models.FileField(
        "Letter of interest",
        upload_to="files/high-altitude-balloon-launch/letter-interest/",
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
        upload_to="files/high-altitude-balloon-launch/cv/",
        validators=[MimetypeValidator('application/pdf')],
        max_length=768,
        help_text="PDF format."
    )

    def __unicode__(self):
        return "High Altitude Balloon Launch"

    def get_application_type(self):
        return "High Altitude Balloon Launch"

    def get_absolute_url(self):
        return reverse(
            'application_update',
            kwargs = {
                'application_type': "high-altitude-balloon-launch",
                'aid': str(self.id)
            }
        )

    class Meta:
        verbose_name_plural = "High altitude balloon launches"


class HighAltitudeBalloonPayload(models.Model):

    # meta
    user = models.ForeignKey(User)
    status = models.BooleanField(default=False)
    updated_by = models.ForeignKey(
        User, verbose_name="Updated by",
        related_name="habp_updated_by",
        editable=False
    )
    date_created = models.DateTimeField(
        "Date Created", auto_now_add=True
    )
    date_updated = models.DateTimeField(
        "Date Updated", auto_now=True
    )
    # core
    letter_interest = models.FileField(
        "Letter of interest",
        upload_to="files/high-altitude-balloon-payload/letter-interest/",
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
        upload_to="files/high-altitude-balloon-payload/cv/",
        validators=[MimetypeValidator('application/pdf')],
        max_length=768,
        help_text="PDF format."
    )

    def __unicode__(self):
        return "High Altitude Balloon Payload"

    def get_application_type(self):
        return "High Altitude Balloon Payload"

    def get_absolute_url(self):
        return reverse(
            'application_update',
            kwargs = {
                'application_type': "high-altitude-balloon-payload",
                'aid': str(self.id)
            }
        )


class ClarkGraduateFellowship(models.Model):

    # meta
    user = models.ForeignKey(User)
    status = models.BooleanField(default=False)
    updated_by = models.ForeignKey(
        User, verbose_name="Updated by",
        related_name="clark_fellowship_updated_by",
        editable=False
    )
    date_created = models.DateTimeField(
        "Date Created", auto_now_add=True
    )
    date_updated = models.DateTimeField(
        "Date Updated", auto_now=True
    )
    # core
    signed_certification = models.FileField(
        upload_to="files/graduate/clark-fellow/signed-certification/",
        validators=[MimetypeValidator('application/pdf')],
        max_length=768,
        help_text=mark_safe('''
            Before beginning the application process,
            please print, obtain signatures, and scan the<br>
            <a href="https://www.carthage.edu/live/files/1365-pdf" target="_blank">
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
        help_text="In Dollars",
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
        upload_to="files/graduate/clark-fellow/proposal/",
        validators=[MimetypeValidator('application/pdf')],
        max_length=768,
        help_text="PDF format."
    )
    cv = models.FileField(
        "Résumé",
        upload_to="files/graduate/clark-fellow/cv/",
        validators=[MimetypeValidator('application/pdf')],
        max_length=768,
        help_text="PDF format."
    )
    budget = models.FileField(
        upload_to="files/graduate/clark-fellow/budget/",
        validators=[MimetypeValidator('application/pdf')],
        max_length=768,
        help_text="PDF format."
    )
    undergraduate_transcripts = models.FileField(
        upload_to="files/graduate/clark-fellow/transcripts/undergraduate/",
        validators=[MimetypeValidator('application/pdf')],
        max_length=768,
        help_text="PDF format."
    )
    graduate_transcripts = models.FileField(
        upload_to="files/graduate/clark-fellow/transcripts/graduate/",
        validators=[MimetypeValidator('application/pdf')],
        max_length=768,
        help_text="PDF format."
    )
    recommendation_1 = models.FileField(
        "Recommendation letter 1",
        upload_to="files/graduate/fellowship/recommendation/",
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
        "Recommendation letter 1",
        upload_to="files/graduate/fellowship/recommendation/",
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
        return "Dr. Laurel Salton Clark Memorial Fellowship"

    def get_absolute_url(self):
        return reverse(
            'application_update',
            kwargs = {
                'application_type': "clark-graduate-fellowship",
                'aid': str(self.id)
            }
        )


class GraduateFellowship(models.Model):

    # meta
    user = models.ForeignKey(User)
    status = models.BooleanField(default=False)
    updated_by = models.ForeignKey(
        User, verbose_name="Updated by",
        related_name="graduate_fellowship_updated_by",
        editable=False
    )
    date_created = models.DateTimeField(
        "Date Created", auto_now_add=True
    )
    date_updated = models.DateTimeField(
        "Date Updated", auto_now=True
    )
    # core
    signed_certification = models.FileField(
        upload_to="files/graduate/fellowship/signed-certification/",
        validators=[MimetypeValidator('application/pdf')],
        max_length=768,
        help_text=mark_safe('''
            Before beginning the application process,
            please print, obtain signatures, and scan the<br>
            <a href="https://www.carthage.edu/live/files/1365-pdf" target="_blank">
            signed certification document
            </a>
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
        help_text="In Dollars",
        null=True,blank=True
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
        upload_to="files/graduate/fellowship/proposal/",
        validators=[MimetypeValidator('application/pdf')],
        max_length=768,
        help_text="PDF format."
    )
    cv = models.FileField(
        "Résumé",
        upload_to="files/graduate/fellowship/cv/",
        validators=[MimetypeValidator('application/pdf')],
        max_length=768,
        help_text="PDF format."
    )
    budget = models.FileField(
        upload_to="files/graduate/fellowship/budget/",
        validators=[MimetypeValidator('application/pdf')],
        max_length=768,
        help_text="PDF format."
    )
    undergraduate_transcripts = models.FileField(
        upload_to="files/graduate/fellowship/transcripts/undergraduate/",
        validators=[MimetypeValidator('application/pdf')],
        max_length=768,
        help_text="PDF format."
    )
    graduate_transcripts = models.FileField(
        upload_to="files/graduate/fellowship/transcripts/graduate/",
        validators=[MimetypeValidator('application/pdf')],
        max_length=768,
        help_text="PDF format."
    )
    recommendation_1 = models.FileField(
        "Recommendation letter 1",
        upload_to="files/graduate/fellowship/recommendation/",
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
        "Recommendation letter 1",
        upload_to="files/graduate/fellowship/recommendation/",
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
        return "Graduate Fellowship"

    def get_absolute_url(self):
        return reverse(
            'application_update',
            kwargs = {
                'application_type': "graduate-fellowship",
                'aid': str(self.id)
            }
        )


class UndergraduateResearch(models.Model):

    # meta
    user = models.ForeignKey(User)
    status = models.BooleanField(default=False)
    updated_by = models.ForeignKey(
        User, verbose_name="Updated by",
        related_name="undergraduate_research_updated_by",
        editable=False
    )
    date_created = models.DateTimeField(
        "Date Created", auto_now_add=True
    )
    date_updated = models.DateTimeField(
        "Date Updated", auto_now=True
    )
    # core
    signed_certification = models.FileField(
        upload_to="files/undergraduate/research/signed-certification/",
        validators=[MimetypeValidator('application/pdf')],
        max_length=768,
        help_text=mark_safe('''
            Before beginning the application process,
            please print, obtain signatures, and scan the<br>
            <a href="https://spacegrant.carthage.edu/live/files/1347-pdf" target="_blank">
            signed certification document
            </a>
        ''')
    )
    project_title = models.CharField(
        "Title of project", max_length=255
    )
    funds_requested = models.IntegerField(help_text="In Dollars")
    funds_authorized = models.IntegerField(
        help_text="In Dollars",
        null=True,blank=True
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
        upload_to="files/undergraduate/research/proposal/",
        validators=[MimetypeValidator('application/pdf')],
        max_length=768,
        help_text="PDF format."
    )
    high_school_transcripts = models.FileField(
        upload_to="files/undergraduate/research/transcripts/high-school/",
        validators=[MimetypeValidator('application/pdf')],
        max_length=768,
        null=True,blank=True,
        help_text="First and second year students only. PDF format."
    )
    undergraduate_transcripts = models.FileField(
        upload_to="files/undergraduate/research/transcripts/undergraduate/",
        validators=[MimetypeValidator('application/pdf')],
        max_length=768,
        help_text="PDF format."
    )
    wsgc_advisor_recommendation = models.FileField(
        "Faculty Research Advisor Recommendation Letter",
        upload_to="files/undergraduate/scholarship/wsgc-advisor-recommendation/",
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
        "Additional Letter of Recommendation (faculty member or other professional reference)",
        upload_to="files/undergraduate/scholarship/recommendation/",
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
        return "Undergraduate Research"

    def get_absolute_url(self):
        return reverse(
            'application_update',
            kwargs = {
                'application_type': "undergraduate-research",
                'aid': str(self.id)
            }
        )


class UndergraduateScholarship(models.Model):

    # meta
    user = models.ForeignKey(User)
    status = models.BooleanField(default=False)
    updated_by = models.ForeignKey(
        User, verbose_name="Updated by",
        related_name="undergraduate_scholarship_updated_by",
        editable=False
    )
    date_created = models.DateTimeField(
        "Date Created", auto_now_add=True
    )
    date_updated = models.DateTimeField(
        "Date Updated", auto_now=True
    )
    # core
    signed_certification = models.FileField(
        upload_to="files/undergraduate/scholarship/signed-certification/",
        validators=[MimetypeValidator('application/pdf')],
        max_length=768,
        help_text=mark_safe('''
            Before beginning the application process,
            please print, obtain signatures, and scan the<br>
            <a href="https://spacegrant.carthage.edu/live/files/1347-pdf" target="_blank">
            signed certification document
            </a>
        ''')
    )
    statement = models.FileField(
        upload_to="files/undergraduate/scholarship/statement/",
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
        upload_to="files/undergraduate/scholarship/transcripts/high-school/",
        validators=[MimetypeValidator('application/pdf')],
        max_length=768,
        null=True,blank=True,
        help_text="First and second year students only. PDF format."
    )
    undergraduate_transcripts = models.FileField(
        upload_to="files/undergraduate/scholarship/transcripts/undergraduate/",
        validators=[MimetypeValidator('application/pdf')],
        max_length=768,
        help_text="PDF format."
    )
    wsgc_advisor_recommendation = models.FileField(
        "Faculty Research Advisor Recommendation Letter",
        upload_to="files/undergraduate/scholarship/wsgc-advisor-recommendation/",
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
        "Additional Letter of Recommendation (faculty member or other professional reference)",
        upload_to="files/undergraduate/scholarship/recommendation/",
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

    def get_absolute_url(self):
        return reverse(
            'application_update',
            kwargs = {
                'application_type': "undergraduate-scholarship",
                'aid': str(self.id)
            }
        )


