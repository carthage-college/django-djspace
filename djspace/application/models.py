# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe

from djtools.fields import BINARY_CHOICES, SALUTATION_TITLES, STATE_CHOICES
from djtools.fields import GENDER_CHOICES
from djtools.fields.format_checker import ContentTypeRestrictedFileField

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
    letter_interest = ContentTypeRestrictedFileField(
        "Letter of interest",
        upload_to="files/high-altitude-balloon-launch/letter-interest/",
        content_types=['application/pdf'],
        help_text="PDF format"
    )
    cv = ContentTypeRestrictedFileField(
        "Résumé",
        upload_to="files/high-altitude-balloon-launch/cv/",
        content_types=['application/pdf'],
        help_text="PDF format"
    )

    def __unicode__(self):
        return "High Altitude Balloon Launch"

    def get_absolute_url(self):
        return reverse(
            'application_update',
            kwargs = {
                'app_type': "high-altitude-balloon-launch",
                'aid': str(self.id)
            }
        )


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
    letter_interest = ContentTypeRestrictedFileField(
        "Letter of interest",
        upload_to="files/high-altitude-balloon-payload/letter-interest/",
        content_types=['application/pdf'],
        help_text="PDF format"
    )
    cv = ContentTypeRestrictedFileField(
        "Résumé",
        upload_to="files/high-altitude-balloon-payload/cv/",
        content_types=['application/pdf'],
        help_text="PDF format"
    )

    def __unicode__(self):
        return "High Altitude Balloon Payload"

    def get_absolute_url(self):
        return reverse(
            'application_update',
            kwargs = {
                'app_type': "high-altitude-balloon-payload",
                'aid': str(self.id)
            }
        )


class ClarkFellowship(models.Model):

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
    anticipating_funding = models.CharField(
        "Are you anticipating other funding this year?",
        max_length=4,
        choices=BINARY_CHOICES
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
    synopsis = models.TextField()
    proposal = ContentTypeRestrictedFileField(
        upload_to="files/graduate/clark-fellow/proposal/",
        content_types=['application/pdf'],
        help_text="PDF format"
    )
    cv = ContentTypeRestrictedFileField(
        "Résumé",
        upload_to="files/graduate/clark-fellow/cv/",
        content_types=['application/pdf'],
        help_text="PDF format"
    )
    budget = ContentTypeRestrictedFileField(
        upload_to="files/graduate/clark-fellow/budget/",
        content_types=['application/pdf'],
        help_text="PDF format"
    )
    undergraduate_transcripts = ContentTypeRestrictedFileField(
        upload_to="files/graduate/clark-fellow/transcripts/undergraduate/",
        content_types=['application/pdf'],
        help_text="PDF format"
    )
    graduate_transcripts = ContentTypeRestrictedFileField(
        upload_to="files/graduate/clark-fellow/transcripts/graduate/",
        help_text="PDF format"
    )
    recommendation = ContentTypeRestrictedFileField(
        upload_to="files/graduate/clark-fellow/recommendation/",
        content_types=['application/pdf'],
        help_text="""
            PDF format:
            Cannot be the same as the WSGC recommendation
        """
    )
    signed_certification = ContentTypeRestrictedFileField(
        upload_to="files/graduate/clark-fellow/signed-certification/",
        content_types=['application/pdf'],
        help_text=mark_safe('''
            <a href="https://www.carthage.edu/live/files/1365-pdf">
            Signed certification document
            </a>
        ''')
    )

    def __unicode__(self):
        return "Clark Fellowship&mdash;%s" % self.project_title

    def get_absolute_url(self):
        return reverse(
            'application_update',
            kwargs = {
                'app_type': "clark-fellowship",
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
    anticipating_funding = models.CharField(
        "Are you anticipating other funding this year?",
        max_length=4,
        choices=BINARY_CHOICES
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
    synopsis = models.TextField()
    proposal = ContentTypeRestrictedFileField(
        upload_to="files/graduate/fellowship/proposal/",
        content_types=['application/pdf'],
        help_text="PDF format"
    )
    cv = ContentTypeRestrictedFileField(
        "Résumé",
        upload_to="files/graduate/fellowship/cv/",
        content_types=['application/pdf'],
        help_text="PDF format"
    )
    budget = ContentTypeRestrictedFileField(
        upload_to="files/graduate/fellowship/budget/",
        content_types=['application/pdf'],
        help_text="PDF format"
    )
    undergraduate_transcripts = ContentTypeRestrictedFileField(
        upload_to="files/graduate/fellowship/transcripts/undergraduate/",
        content_types=['application/pdf'],
        help_text="PDF format"
    )
    graduate_transcripts = ContentTypeRestrictedFileField(
        upload_to="files/graduate/fellowship/transcripts/graduate/",
        content_types=['application/pdf'],
        help_text="PDF format"
    )
    recommendation = ContentTypeRestrictedFileField(
        upload_to="files/graduate/fellowship/recommendation/",
        content_types=['application/pdf'],
        help_text="""
            PDF format:
            Cannot be the same as the WSGC recommendation
        """
    )
    signed_certification = ContentTypeRestrictedFileField(
        upload_to="files/graduate/fellowship/signed-certification/",
        content_types=['application/pdf'],
        help_text=mark_safe('''
            <a href="https://www.carthage.edu/live/files/1365-pdf">
            Signed certification document
            </a>
        ''')
    )

    def __unicode__(self):
        return "Graduate Fellowship: %s" % self.project_title

    def get_absolute_url(self):
        return reverse(
            'application_update',
            kwargs = {
                'app_type': "graduate-fellowship",
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
    synopsis = models.TextField()
    proposal = ContentTypeRestrictedFileField(
        upload_to="files/undergraduate/research/proposal/",
        content_types=['application/pdf'],
        help_text="PDF format"
    )
    high_school_transcripts = ContentTypeRestrictedFileField(
        upload_to="files/undergraduate/research/transcripts/high-school/",
        content_types=['application/pdf'],
        help_text="PDF format"
    )
    undergraduate_transcripts = ContentTypeRestrictedFileField(
        upload_to="files/undergraduate/research/transcripts/undergraduate/",
        content_types=['application/pdf'],
        help_text="PDF format"
    )
    wsgc_advisor_recommendation = ContentTypeRestrictedFileField(
        upload_to="files/undergraduate/research/wsgc-advisor-recommendation/",
        content_types=['application/pdf'],
        help_text="PDF format"
    )
    recommendation = ContentTypeRestrictedFileField(
        upload_to="files/undergraduate/research/recommendation/",
        content_types=['application/pdf'],
        help_text="""
            PDF format:
            Cannot be the same as the WSGC recommendation
        """
    )
    signed_certification = ContentTypeRestrictedFileField(
        upload_to="files/undergraduate/research/signed-certification/",
        content_types=['application/pdf'],
        help_text=mark_safe('''
            <a href="https://www.carthage.edu/live/files/1365-pdf">
            Signed certification document
            </a>
        ''')
    )

    def __unicode__(self):
        return "Undergraduate Research: %s" % self.project_title

    def get_absolute_url(self):
        return reverse(
            'application_update',
            kwargs = {
                'app_type': "undergraduate-research",
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
    statement = models.TextField()
    high_school_transcripts = ContentTypeRestrictedFileField(
        upload_to="files/undergraduate/scholarship/transcripts/high-school/",
        content_types=['application/pdf'],
        help_text="PDF format"
    )
    undergraduate_transcripts = ContentTypeRestrictedFileField(
        upload_to="files/undergraduate/scholarship/transcripts/undergraduate/",
        content_types=['application/pdf'],
        help_text="PDF format"
    )
    wsgc_advisor_recommendation = ContentTypeRestrictedFileField(
        upload_to="files/undergraduate/scholarship/wsgc-advisor-recommendation/",
        content_types=['application/pdf'],
        help_text="PDF format"
    )
    recommendation = ContentTypeRestrictedFileField(
        upload_to="files/undergraduate/scholarship/recommendation/",
        content_types=['application/pdf'],
        help_text="""
            PDF format:
            Cannot be the same as the WSGC recommendation
        """
    )
    signed_certification = ContentTypeRestrictedFileField(
        upload_to="files/undergraduate/scholarship/signed-certification/",
        content_types=['application/pdf'],
        help_text=mark_safe('''
            <a href="https://www.carthage.edu/live/files/1365-pdf">
            Signed certification document
            </a>
        ''')
    )

    def __unicode__(self):
        return "Undergraduate Scholarship"

    def get_absolute_url(self):
        return reverse(
            'application_update',
            kwargs = {
                'app_type': "undergraduate-scholarship",
                'aid': str(self.id)
            }
        )


