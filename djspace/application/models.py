# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe

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
        help_text="PDF format"
    )
    cv = models.FileField(
        "Résumé",
        upload_to="files/high-altitude-balloon-launch/cv/",
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
    letter_interest = models.FileField(
        "Letter of interest",
        upload_to="files/high-altitude-balloon-payload/letter-interest/",
        help_text="PDF format"
    )
    cv = models.FileField(
        "Résumé",
        upload_to="files/high-altitude-balloon-payload/cv/",
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
    proposal = models.FileField(
        upload_to="files/graduate/clark-fellow/proposal/",
        help_text="PDF format"
    )
    cv = models.FileField(
        "Résumé",
        upload_to="files/graduate/clark-fellow/cv/",
        help_text="PDF format"
    )
    budget = models.FileField(
        upload_to="files/graduate/clark-fellow/budget/",
        help_text="PDF format"
    )
    undergraduate_transcripts = models.FileField(
        upload_to="files/graduate/clark-fellow/undergraduate_transcripts/",
        help_text="PDF format"
    )
    graduate_transcripts = models.FileField(
        upload_to="files/graduate/clark-fellow/graduate_transcripts/",
        help_text="PDF format"
    )
    recommendation = models.FileField(
        upload_to="files/graduate/clark-fellow/recommendation/",
        help_text="""
            PDF format:
            Cannot be the same as the WSGC recommendation
        """
    )
    signed_certification = models.FileField(
        upload_to="files/graduate/clark-fellow/signed_certification/",
        help_text=mark_safe('''
            <a href="https://www.carthage.edu/live/files/1365-pdf">
            Signed certification document
            </a>
        ''')
    )

    def __unicode__(self):
        return "Clark Fellowship: %s" % self.project_title

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
    proposal = models.FileField(
        upload_to="files/graduate/fellowship/proposal/",
        help_text="PDF format"
    )
    cv = models.FileField(
        "Résumé",
        upload_to="files/graduate/fellowship/cv/",
        help_text="PDF format"
    )
    budget = models.FileField(
        upload_to="files/graduate/fellowship/budget/",
        help_text="PDF format"
    )
    undergraduate_transcripts = models.FileField(
        upload_to="files/graduate/fellowship/undergraduate_transcripts/",
        help_text="PDF format"
    )
    graduate_transcripts = models.FileField(
        upload_to="files/graduate/fellowship/graduate_transcripts/",
        help_text="PDF format"
    )
    recommendation = models.FileField(
        upload_to="files/graduate/fellowship/recommendation/",
        help_text="""
            PDF format:
            Cannot be the same as the WSGC recommendation
        """
    )
    signed_certification = models.FileField(
        upload_to="files/graduate/fellowship/signed_certification/",
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
    proposal = models.FileField(
        upload_to="files/undergraduate/research/proposal/",
        help_text="PDF format"
    )
    high_school_transcripts = models.FileField(
        upload_to="files/undergraduate/research/undergraduate_transcripts/",
        help_text="PDF format"
    )
    undergraduate_transcripts = models.FileField(
        upload_to="files/undergraduate/research/undergraduate_transcripts/",
        help_text="PDF format"
    )
    wsgc_advisor_recommendation = models.FileField(
        upload_to="files/undergraduate/research/wsgc_advisor_recommendation/",
        help_text="PDF format"
    )
    recommendation = models.FileField(
        upload_to="files/undergraduate/research/recommendation/",
        help_text="""
            PDF format:
            Cannot be the same as the WSGC recommendation
        """
    )
    signed_certification = models.FileField(
        upload_to="files/undergraduate/research/signed_certification/",
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
    high_school_transcripts = models.FileField(
        upload_to="files/undergraduate/scholarship/high_school_transcripts/",
        help_text="PDF format"
    )
    undergraduate_transcripts = models.FileField(
        upload_to="files/undergraduate/scholarship/undergraduate_transcripts/",
        help_text="PDF format"
    )
    wsgc_advisor_recommendation = models.FileField(
        upload_to="files/undergraduate/scholarship/wsgc_advisor_recommendation/",
        help_text="PDF format"
    )
    recommendation = models.FileField(
        upload_to="files/undergraduate/scholarship/recommendation/",
        help_text="""
            PDF format:
            Cannot be the same as the WSGC recommendation
        """
    )
    signed_certification = models.FileField(
        upload_to="files/undergraduate/scholarship/signed_certification/",
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


