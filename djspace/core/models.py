# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.contrib.auth.models import User
from allauth.account.signals import user_signed_up
from allauth.account.models import EmailAddress
from taggit.managers import TaggableManager
from gm2m import GM2MField

from djspace.core.utils import registration_notify, get_email_auxiliary
from djspace.core.utils import get_profile_status

from djtools.fields import BINARY_CHOICES, YES_NO_DECLINE, STATE_CHOICES
from djtools.fields import GENDER_CHOICES, SALUTATION_TITLES
from djtools.utils.convert import str_to_class
from djtools.fields.validators import MimetypeValidator

from datetime import date, datetime

import os

REG_TYPE = (
    ('','----select----'),
    ('Undergraduate','Undergraduate'),
    ('Graduate','Graduate'),
    ('Faculty','Faculty'),
    ('Professional','Professional')
)

BIRTH_YEAR_CHOICES = [x for x in reversed(xrange(1926,date.today().year -11))]
DISABILITY_CHOICES = (
    ('','----select----'),
    ("I do not have a disability", "I do not have a disability"),
    ("I do not wish to identify my disability status",
     "I do not wish to identify my disability status"),
    ("Hearing", "Hearing"),
    ("Vision", "Vision"),
    ("Missing Extremeties", "Missing Extremeties"),
    ("Paralysis", "Paralysis"),
    ("Other Impairments", "Other Impairments"),
    ("I have a disability, but it is not listed",
     "I have a disability, but it is not listed")
)
EMPLOYMENT_CHOICES = (
    ('','----select----'),
    ("Employed with NASA/JPL", "Employed with NASA/JPL"),
    ("Employed with an AerospaceContractor",
     "Employed with an AerospaceContractor"),
    ("Employed in a STEM field (Non-Aerospace field)",
     "Employed in a STEM field (Non-Aerospace field)"),
    ("Employed in K-12 STEM academic field",
     "Employed in K-12 STEM academic field"),
    ("Employed in 'Other' STEM academic field",
     "Employed in 'Other' STEM academic field"),
    ("Other (e.g. non-STEM employment, non-STEM academic degree, unemployed)",
     "Other (e.g. non-STEM employment, non-STEM academic degree, unemployed)"),
)

from uuid import uuid4


def upload_to_path(self, filename):
    """
    Generates the path as a string for file field.
    """

    ext = filename.split('.')[-1]
    # set filename as random string
    filename = '{}.{}'.format(uuid4().hex, ext)
    sendero = "{}/{}/".format(
        self.get_file_path(), self.user.id
    )
    return os.path.join(sendero, filename)


class Base(models.Model):
    """
    Abstract model that forms the basis for all registration types
    """

    # meta
    user = models.ForeignKey(User)
    date_created = models.DateTimeField(
        "Date Created", auto_now_add=True
    )
    date_updated = models.DateTimeField(
        "Date Updated", auto_now=True
    )
    updated_by = models.ForeignKey(
        User, verbose_name="Updated by",
        related_name="%(app_label)s_%(class)s_related",
        editable=False
    )

    class Meta:
        abstract = True


class BaseModel(Base):
    """
    Abstract model that forms the basis for all applications.
    Inherts from Base() class.
    """

    status = models.BooleanField(default=False, verbose_name="Funded")

    class Meta:
        abstract = True


class GenericChoice(models.Model):
    """
    For making choices for choice fields for forms
    """
    name = models.CharField(
        max_length=255
    )
    value = models.CharField(
        unique=True, max_length=255
    )
    ranking = models.IntegerField(
        null=True, blank=True, default=0,
        verbose_name="Ranking",
        help_text=
        """
        A number from 0 to 999 to determine this object's position in a list.
        """
    )
    active = models.BooleanField(
        help_text=
        """
        Do you want the field to be visable on your form?
        """,
        verbose_name="Is active?",
        default=True
    )
    tags = TaggableManager()

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['ranking']

def limit_race():
    rids = [
        g.id for g in GenericChoice.objects.filter(
            tags__name__in=["Race"]
        ).order_by("name")
    ]
    return rids

class UserFiles(models.Model):

    user = models.ForeignKey(
        User,
        related_name="user_files",
        editable=False
    )
    mugshot = models.FileField(
        upload_to=upload_to_path,
        #validators=[MimetypeValidator('image/jpeg')],
        max_length=768,
        null=True, blank=True,
        help_text="JPEG format (.jpg)"
    )
    biography = models.FileField(
        upload_to=upload_to_path,
        #validators=[MimetypeValidator('application/pdf')],
        max_length=768,
        null=True, blank=True,
        help_text="PDF format"
    )
    media_release = models.FileField(
        upload_to=upload_to_path,
        #validators=[MimetypeValidator('application/pdf')],
        max_length=768,
        null=True, blank=True,
        help_text="PDF format"
    )
    irs_w9 = models.FileField(
        upload_to=upload_to_path,
        #validators=[MimetypeValidator('application/pdf')],
        max_length=768,
        null=True, blank=True,
        help_text="PDF format"
    )

    def get_file_path(self):
        return "files/users"

class UserProfile(models.Model):

    # meta
    user = models.OneToOneField(
        User, related_name="profile"
    )
    updated_by = models.ForeignKey(
        User, verbose_name="Updated by",
        related_name="user_profile_updated_by",
        editable=False
    )
    date_created = models.DateTimeField(
        "Date Created", auto_now_add=True
    )
    date_updated = models.DateTimeField(
        "Date Updated", auto_now=True
    )
    # core
    salutation = models.CharField(
        max_length=16,
        choices=SALUTATION_TITLES,
        null=True, blank=True
    )
    second_name = models.CharField(
        max_length=30,
        null=True, blank=True
    )
    address1 = models.CharField(
        "Address",
        max_length=128
    )
    address2 = models.CharField(
        "",
        max_length=128,
        null=True, blank=True
    )
    city = models.CharField(
        "City",
        max_length=128
    )
    state = models.CharField(
        "State",
        max_length=2,
        choices=STATE_CHOICES
    )
    postal_code = models.CharField(
        "Zip code",
        max_length=10
    )
    address1_current = models.CharField(
        "Address",
        max_length=128,
        null=True, blank=True
    )
    address2_current = models.CharField(
        "",
        max_length=128,
        null=True, blank=True
    )
    city_current = models.CharField(
        "City",
        max_length=128,
        null=True, blank=True
    )
    state_current = models.CharField(
        "State",
        max_length=2,
        choices=STATE_CHOICES,
        null=True, blank=True
    )
    postal_code_current = models.CharField(
        "Zip code",
        max_length=10,
        null=True, blank=True
    )
    phone_primary = models.CharField(
        verbose_name='Primary phone',
        max_length=12,
        help_text="Format: XXX-XXX-XXXX"
    )
    phone_mobile = models.CharField(
        verbose_name='Cell phone',
        max_length=12,
        help_text="Format: XXX-XXX-XXXX",
        null=True, blank=True
    )
    date_of_birth = models.DateField(
        "Date of birth",
        help_text="Format: mm/dd/yyyy"
    )
    gender = models.CharField(
        max_length=16,
        choices = GENDER_CHOICES
    )
    race = models.ManyToManyField(
        GenericChoice,
        #limit_choices_to={"id__in":limit_race},
        related_name="user_profile_race",
        help_text = 'Check all that apply'
    )
    tribe = models.CharField(
        "Tribe",
        max_length=128,
        null=True, blank=True
    )
    disability = models.CharField(
        "Disability status",
        max_length=64,
        choices=DISABILITY_CHOICES
    )
    disability_specify = models.CharField(
        "Specify if not listed",
        max_length=255,
        null=True, blank=True
    )
    us_citizen = models.CharField(
        "United States Citizen",
        max_length=4,
        choices=BINARY_CHOICES
    )
    employment = models.CharField(
        "Employment status",
        max_length=128,
        choices=EMPLOYMENT_CHOICES
    )
    military = models.CharField(
        "Have you served in the United States military?",
        max_length=4,
        choices=BINARY_CHOICES
    )
    registration_type = models.CharField(
        max_length=32,
        choices=REG_TYPE
    )
    applications = GM2MField(
        'application.HigherEducationInitiatives',
        'application.ResearchInfrastructure',
        'application.AerospaceOutreach',
        'application.SpecialInitiatives',
        'application.RocketLaunchTeam',
        'application.MidwestHighPoweredRocketCompetition',
        'application.CollegiateRocketCompetition',
        'application.FirstNationsRocketCompetition',
        'application.HighAltitudeBalloonLaunch',
        'application.HighAltitudeBalloonPayload',
        'application.ClarkGraduateFellowship',
        'application.GraduateFellowship',
        'application.UndergraduateResearch',
        'application.UndergraduateScholarship',
        'application.NasaCompetition',
        'application.IndustryInternship'
    )

    def __unicode__(self):
        return u"{} {}'s profile".format(
            self.user.first_name, self.user.last_name
        )

    def email_auxiliary(self):
        return get_email_auxiliary(self.user)

    def get_race(self):
        race = ""
        for r in self.race.all():
            race += "{},".format(r)
        return race[:-1]

    def get_registration(self):
        # these imports need to be here, rather than at the top with the others
        from djspace.registration.models import Undergraduate, Graduate
        from djspace.registration.models import Faculty, Professional

        try:
            reg = str_to_class(
                "djspace.registration.models", self.registration_type
            )
            return reg.objects.get(user=self.user)
        except:
            return None

    def save(self, *args, **kwargs):
        if self.id and not get_profile_status(self.user):
            # notify WSGC administrators of registration update
            request = None
            registration_notify(request, "update", self.user)
        super(UserProfile, self).save()


# dispatch ID needs to be unique for each signal handler, nothing more.
# so we can use package plus signal name.
@receiver(user_signed_up, dispatch_uid="allauth.user_signed_up")
def _user_signed_up(request, user, **kwargs):

    # Add secondary email address for the user, and send email confirmation.
    EmailAddress.objects.add_email(
        request, user, request.POST.get("email_secondary"), confirm=True
    )

    # notify WSGC administrators of new user registration
    registration_notify(request, "create", user)


"""
class GenericManyToMany(models.Model):
    from django.contrib.contenttypes.models import ContentType
    gm2m_src = models.ForeignKey(UserProfile)
    gm2m_ct = models.ForeignKey(ContentType)
    gm2m_pk = models.CharField(max_length=16)

    class Meta:
        db_table = 'core_userprofile_applications'
"""

