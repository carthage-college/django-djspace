# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.fields import GenericForeignKey

from djspace.core.utils import get_email_auxiliary, get_start_date
from djspace.core.utils import profile_status, upload_to_path
from djspace.core.utils import registration_notify

from djtools.fields import BINARY_CHOICES, YES_NO_DECLINE, STATE_CHOICES
from djtools.fields import GENDER_CHOICES, SALUTATION_TITLES
from djtools.fields.validators import MimetypeValidator

from gm2m import GM2MField
from allauth.account.signals import user_signed_up
from taggit.managers import TaggableManager

from os.path import join, getmtime, getctime
from datetime import date, datetime
from functools import partial
from uuid import uuid4

import time
import re

FILE_VALIDATORS = [MimetypeValidator('application/pdf')]
PHOTO_VALIDATORS = [MimetypeValidator('image/jpeg')]
REG_TYPE = (
    ('','----select----'),
    ('Undergraduate','Undergraduate'),
    ('Graduate','Graduate'),
    ('Faculty','Faculty'),
    ('Professional','Professional')
)
BIRTH_YEAR_CHOICES = [x for x in reversed(xrange(1926,date.today().year -11))]
PAST_FUNDING_YEAR_CHOICES = [
    (x, x) for x in reversed(xrange(date.today().year-5,date.today().year+1))
]
PAST_FUNDING_YEAR_CHOICES.insert(0,('','---year---'))
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

def _timestamp(obj, field):
    phile = getattr(obj, field, None)
    #path = join(
    #    settings.MEDIA_ROOT, str(phile.name).encode('utf-8', 'ignore')
    #)
    path = join(settings.MEDIA_ROOT, phile.name)
    # ctime() does not refer to creation time on *nix systems,
    # but rather the last time the inode data changed
    #return time.ctime(getctime(path))
    # time.gmtime() returns the time in UTC so we use time.localtime()
    #return time.strftime(
        #'%Y-%m-%d %H:%M:%S', time.localtime(getmtime(path))
    #)

    try:
        ts = datetime.fromtimestamp(
            time.mktime(time.localtime(getmtime(path)))
        )
    except:
        # we might not have the files on dev/staging
        if settings.DEBUG:
            ts = datetime.today()

    return ts


class Photo(models.Model):
    phile = models.ImageField(
        "Photo",
        upload_to = partial(upload_to_path, 'Program_Photo'),
        validators = PHOTO_VALIDATORS,
        max_length = 768,
        help_text = "JPEG only"
    )
    caption = models.TextField(
        null = True, blank = True
    )
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __unicode__(self):
        return u"{}".format(self.caption)

    def user(self):
        return self.content_object.user

    def get_file_path(self):
        return "files/applications"

    def get_slug(self):
        return self.content_object.get_slug()

    def get_file_name(self):
        return u'{}_{}.{}'.format(
            self.content_object.get_code(),
            self.user().last_name, self.user().first_name
        )

    def get_file_timestamp(self):
        return _timestamp(self, 'phile')

    def get_content_type(self):
        return ContentType.objects.get_for_model(self)


class Base(models.Model):
    """
    Abstract model that forms the basis for all registration types and
    program applications (BaseModel)
    """

    class Meta:
        abstract = True

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

    def get_content_type(self):
        return ContentType.objects.get_for_model(self)

    def get_file_name(self):
        return uuid4().hex

    def get_file_timestamp(self, field):
        return _timestamp(self, field)


class BaseModel(Base):
    """
    Abstract model that forms the basis for all applications.
    Inherts from Base() class.
    """

    class Meta:
        abstract = True

    status = models.BooleanField(default=False, verbose_name="Funded")
    funded_code = models.CharField(
        "Funded ID",
        max_length=24,
        null=True, blank=True
    )
    past_funding = models.CharField(
        "Have you received WSGC funding within the past five years?",
        max_length=4,
        choices=BINARY_CHOICES,
        null=True, blank=True
    )
    past_funding_year = models.CharField(
        "If 'Yes', what year?",
        max_length=4,
        # OJO: does not display on django admin listing if choices is set.
        #choices=PAST_FUNDING_YEAR_CHOICES,
        null=True, blank=True
    )
    award_acceptance = models.FileField(
        upload_to = partial(upload_to_path, 'Award_Acceptance'),
        validators=FILE_VALIDATORS,
        max_length=768,
        null=True, blank=True,
        help_text="PDF format"
    )
    interim_report = models.FileField(
        upload_to = partial(upload_to_path, 'Interim_Report'),
        validators=FILE_VALIDATORS,
        max_length=768,
        null=True, blank=True,
        help_text="PDF format"
    )
    final_report = models.FileField(
        upload_to = partial(upload_to_path, 'Final_Report'),
        validators=FILE_VALIDATORS,
        max_length=768,
        null=True, blank=True,
        help_text="PDF format"
    )
    photos = GenericRelation(Photo)

    def multi_year(self):
        #return False
        return True

    def get_file_path(self):
        return "files/applications"

    def get_file_name(self):
        return u'{}_{}.{}'.format(
            self.get_code(),self.user.last_name,self.user.first_name
        )

    def get_details_url(self):

        return reverse(
            'application_print',
            kwargs={'application_type':self.get_slug(),'aid': self.id},
        )


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
        #app_label = "genericchoice"
        ordering = ['ranking']

def limit_race():
    rids = [
        g.id for g in GenericChoice.objects.filter(
            tags__name__in=["Race"]
        ).order_by("name")
    ]
    return rids


class UserFiles(models.Model):

    user = models.OneToOneField(
        User,
        related_name="user_files",
        editable=False
    )
    mugshot = models.FileField(
        "Photo",
        upload_to = partial(upload_to_path, 'Photo'),
        validators=PHOTO_VALIDATORS,
        max_length=768,
        null=True, blank=True,
        help_text="JPEG format (.jpg)"
    )
    biography = models.FileField(
        upload_to = partial(upload_to_path, 'Bio'),
        validators=FILE_VALIDATORS,
        max_length=768,
        null=True, blank=True,
        help_text="PDF format"
    )
    media_release = models.FileField(
        upload_to = partial(upload_to_path, 'Media_Release'),
        validators=FILE_VALIDATORS,
        max_length=768,
        null=True, blank=True,
        help_text="""
            Media release forms must contain a hand-written signature to be
            accepted by NASA. File must be in PDF format.
        """
    )
    irs_w9 = models.FileField(
        upload_to = partial(upload_to_path, 'W9'),
        validators=FILE_VALIDATORS,
        max_length=768,
        null=True, blank=True,
        help_text="PDF format"
    )

    class Meta:
        db_table = "core_userfiles"

    def get_file_path(self):
        return 'files'

    def get_slug(self):
        return "users"

    def get_file_name(self):
        return u'{}.{}'.format(
            self.user.last_name,self.user.first_name
        )

    def get_file_timestamp(self, field):
        return _timestamp(self, field)

    def status(self, field):
        timestamp = self.get_file_timestamp(field)
        s = True
        if timestamp < get_start_date():
            s = False
        return s

    def __unicode__(self):
        return u'User Profile File'


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
        'application.StemBridgeScholarship',
        'application.UndergraduateResearch',
        'application.UndergraduateScholarship',
        'application.NasaCompetition',
        'application.IndustryInternship',
        'application.ProfessionalProgramStudent'
    )

    class Meta:
        #app_label = "userprofile"
        db_table = "core_userprofile"

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
        import django
        from djspace.registration.models import Undergraduate, Graduate
        from djspace.registration.models import Faculty, Professional

        if self.registration_type:
            mod = django.apps.apps.get_model(
                app_label='registration', model_name=self.registration_type
            )
            return mod.objects.get(user=self.user)
        else:
            return None

    def save(self, *args, **kwargs):
        if self.id and not profile_status(self.user):
            # notify WSGC administrators of registration update
            request = None
            registration_notify(request, "update", self.user)
        super(UserProfile, self).save()


# dispatch ID needs to be unique for each signal handler, nothing more.
# so we can use package plus signal name.
@receiver(user_signed_up, dispatch_uid="allauth.user_signed_up")
def _user_signed_up(request, user, **kwargs):

    from allauth.account.models import EmailAddress
    # Add secondary email address for the user, and send email confirmation.
    # try/except for the rare cases when someone tries to register after they
    # have already done so and the email they are attempting to use somehow
    # slipped past our form clean() method.
    try:
        EmailAddress.objects.add_email(
            request, user, request.POST.get("email_secondary"), confirm=True
        )
    except:
        pass
    # create UserFiles() obj for storing uploaded files after grant approval
    uf = UserFiles(user=user)
    uf.save()
    # notify WSGC administrators of new user registration
    registration_notify(request, "create", user)

