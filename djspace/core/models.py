# -*- coding: utf-8 -*-

import time
from datetime import date
from datetime import datetime
from functools import partial
from os.path import getmtime
from os.path import join
from uuid import uuid4

from allauth.account.signals import user_signed_up
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.core.validators import FileExtensionValidator
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from djspace.core.utils import get_email_auxiliary
from djspace.core.utils import get_start_date
from djspace.core.utils import profile_status
from djspace.core.utils import registration_notify
from djspace.core.utils import upload_to_path
from djtools.fields import BINARY_CHOICES
from djtools.fields import GENDER_CHOICES
from djtools.fields import SALUTATION_TITLES
from djtools.fields import STATE_CHOICES
from djtools.fields.validators import MimetypeValidator
from gm2m import GM2MField
from taggit.managers import TaggableManager


# comment out for migrations
FILE_VALIDATORS = [MimetypeValidator('application/pdf')]
PHOTO_VALIDATORS = [MimetypeValidator('image/jpeg')]
ALLOWED_EXTENSIONS = [
    'doc',
    'docx',
    'xls',
    'xlsx',
    'pdf',
    'tar',
    'zip',
    'gzip',
    'jpg',
    'jpeg',
    'png',
    'ppt',
    'pptx',
]

REG_TYPE = (
    ('', "----select----"),
    ('HighSchool', "High School"),
    ('Undergraduate', "Undergraduate"),
    ('Graduate', "Graduate"),
    ('Faculty', "Faculty"),
    ('GrantsOfficer', "Grants Officer"),
    ('Professional', "Professional"),
)

BIRTH_YEAR_CHOICES = list(reversed(range(1926, date.today().year - 11)))
PAST_FUNDING_YEAR_CHOICES = [
    (yr, yr) for yr in reversed(range(date.today().year - 5, date.today().year + 1))
]
PAST_FUNDING_YEAR_CHOICES.insert(0, ('', "---year---"))
DISABILITY_CHOICES = (
    ('', "----select----"),
    ('I do not have a disability', "I do not have a disability"),
    (
        'I do not wish to identify my disability status',
        "I do not wish to identify my disability status",
    ),
    ('Hearing', "Hearing"),
    ('Vision', "Vision"),
    ('Missing Extremeties', "Missing Extremeties"),
    ('Paralysis', "Paralysis"),
    ('Other Impairments', "Other Impairments"),
    (
        'I have a disability, but it is not listed',
        "I have a disability, but it is not listed",
    ),
)
EMPLOYMENT_CHOICES = (
    ('', "----select----"),
    ('Employed with NASA/JPL', "Employed with NASA/JPL"),
    (
        'Employed with an AerospaceContractor',
        "Employed with an AerospaceContractor",
    ),
    (
        'Employed in a STEM field (Non-Aerospace field)',
        "Employed in a STEM field (Non-Aerospace field)",
    ),
    (
        'Employed in K-12 STEM academic field',
        "Employed in K-12 STEM academic field",
    ),
    (
        'Employed in other STEM academic field',
        "Employed in other STEM academic field",
    ),
    (
        'Other (e.g. non-STEM employment, non-STEM academic degree, unemployed)',
        "Other (e.g. non-STEM employment, non-STEM academic degree, unemployed)",
    ),
    ('N/A', "N/A"),
)
FUNDING_CHOICES = (
    ('', "----select----"),
    ('WSGC', 'WSGC'),
    ('Federal', 'Federal'),
    ('Not Applicable', 'Not Applicable'),
)


def _timestamp(phile, field):
    """Obtain the timestamp from the file system."""
    attr = getattr(phile, field, None)
    path = join(settings.MEDIA_ROOT, attr.name)
    # ctime() does not refer to creation time on *nix systems,
    # but rather the last time the inode data changed: time.ctime(getctime(path))
    # time.gmtime() returns the time in UTC so we use time.localtime()

    try:
        ts = datetime.fromtimestamp(
            time.mktime(time.localtime(getmtime(path))),
        )
    except Exception:
        # we might not have the files on dev/staging
        ts = datetime.today()

    return ts


def limit_race():
    """Obtain the IDs for race generic choices."""
    return [
        genchoi.id for genchoi in GenericChoice.objects.filter(
            tags__name__in=['Race'],
        ).order_by('name')
    ]


class Photo(models.Model):
    """Generic class for a photo image file."""

    phile = models.ImageField(
        "Photo",
        upload_to=partial(upload_to_path, 'Program_Photo'),
        validators=PHOTO_VALIDATORS,
        max_length=768,
        help_text="JPEG only",
    )
    caption = models.TextField(null=True, blank=True)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        """Default display value in unicode encoding."""
        return "{0}".format(self.caption)

    def user(self):
        """Return the user owner of the object."""
        return self.content_object.user

    def get_file_path(self):
        """Return the path prefix for the file."""
        return 'files/applications'

    def get_slug(self):
        """Return the slug for the associated content object."""
        return self.content_object.get_slug()

    def get_file_name(self):
        """Return the file name based on content object code and user's name."""
        return '{0}_{1}.{2}'.format(
            self.content_object.get_code(),
            self.user().last_name,
            self.user().first_name,
        )

    def get_file_timestamp(self):
        """Return the timestamp for the phile. i.e. when it was created."""
        return _timestamp(self, 'phile')

    def get_content_type(self):
        """Return the content type of the associciated object."""
        return ContentType.objects.get_for_model(self)


class Base(models.Model):
    """
    Abstract model that forms the basis for all models.

    Registration types and program applications (BaseModel).
    """

    class Meta:
        """Attributes about the data model and admin options."""

        abstract = True

    # meta
    user = models.ForeignKey(User)
    date_created = models.DateTimeField("Date Created", auto_now_add=True)
    date_updated = models.DateTimeField("Date Updated", auto_now=True)
    updated_by = models.ForeignKey(
        User,
        verbose_name="Updated by",
        related_name='%(app_label)s_%(class)s_related',
        editable=False,
    )

    def get_content_type(self):
        """Return the content type of the associciated object."""
        return ContentType.objects.get_for_model(self)

    def get_file_name(self):
        """Return the file name which is a uuid4 hex."""
        return uuid4().hex

    def get_file_timestamp(self, field):
        """Return the timestamp for the phile. i.e. when it was created."""
        return _timestamp(self, field)


class BaseModel(Base):
    """
    Abstract model that forms the basis for all applications.

    Inherts from Base() class.
    """

    class Meta:
        """Attributes about the data model and admin options."""

        abstract = True

    status = models.BooleanField(default=False, verbose_name="Funded")
    complete = models.BooleanField(default=False, verbose_name="Completed")
    funded_code = models.CharField(
        "Funded ID",
        max_length=24,
        null=True,
        blank=True,
    )
    past_funding = models.CharField(
        "Have you received WSGC funding within the past five years?",
        max_length=4,
        choices=BINARY_CHOICES,
        null=True,
        blank=True,
    )
    past_funding_year = models.CharField(
        "If 'Yes', what year?",
        max_length=4,
        # OJO: does not display on django admin listing if
        # choices is set to PAST_FUNDING_YEAR_CHOICES
        null=True,
        blank=True,
    )
    anticipating_funding = models.CharField(
        "Are you anticipating other funding this year?",
        max_length=32,
        choices=FUNDING_CHOICES,
        help_text="Grants/Scholarships/etc.",
    )
    award_acceptance = models.FileField(
        upload_to=partial(upload_to_path, 'Award_Acceptance'),
        validators=FILE_VALIDATORS,
        max_length=768,
        null=True,
        blank=True,
        help_text="PDF format",
    )
    interim_report = models.FileField(
        upload_to=partial(upload_to_path, 'Interim_Report'),
        validators=FILE_VALIDATORS,
        max_length=768,
        null=True,
        blank=True,
        help_text="PDF format",
    )
    final_report = models.FileField(
        upload_to=partial(upload_to_path, 'Final_Report'),
        validators=FILE_VALIDATORS,
        max_length=768,
        null=True,
        blank=True,
        help_text="PDF format",
    )
    other_file = models.FileField(
        "Ancillary File 1",
        upload_to=partial(upload_to_path, 'Other_File'),
        validators=[FileExtensionValidator(allowed_extensions=ALLOWED_EXTENSIONS)],
        help_text=ALLOWED_EXTENSIONS,
        max_length=768,
        null=True,
        blank=True,
    )
    other_file2 = models.FileField(
        "Ancillary File 2",
        upload_to=partial(upload_to_path, 'Other_File2'),
        validators=[FileExtensionValidator(allowed_extensions=ALLOWED_EXTENSIONS)],
        help_text=ALLOWED_EXTENSIONS,
        max_length=768,
        null=True,
        blank=True,
    )
    other_file3 = models.FileField(
        "Ancillary File 3",
        upload_to=partial(upload_to_path, 'Other_File3'),
        validators=[FileExtensionValidator(allowed_extensions=ALLOWED_EXTENSIONS)],
        help_text=ALLOWED_EXTENSIONS,
        max_length=768,
        null=True,
        blank=True,
    )
    url1 = models.CharField(
        max_length=768,
        null=True,
        blank=True,
        help_text="Other URL for linking to files or photos",
    )
    url2 = models.CharField(
        max_length=768,
        null=True,
        blank=True,
        help_text="Other URL for linking to files or photos",
    )
    url3 = models.CharField(
        max_length=768,
        null=True,
        blank=True,
        help_text="Other URL for linking to files or photos",
    )
    photos = GenericRelation(Photo)

    def multi_year(self):
        """Report that this application spans multiple grant cycles."""
        return True

    def get_file_path(self):
        """Return the path prefix for the file."""
        return 'files/applications'

    def get_file_name(self):
        """Return the file name based on content object code and user's name."""
        return '{0}_{1}.{2}'.format(
            self.get_code(), self.user.last_name, self.user.first_name,
        )

    def get_details_url(self):
        """Return the URL for the details view for this object."""
        return reverse(
            'application_print',
            kwargs={'application_type': self.get_slug(), 'aid': self.id},
        )


class GenericChoice(models.Model):
    """For making choices for choice fields for forms."""

    name = models.CharField(max_length=255)
    value = models.CharField(unique=True, max_length=255)
    ranking = models.IntegerField(
        "Ranking",
        null=True,
        blank=True,
        default=0,
        help_text="""
            A number from 0 to 999 to determine this object's position in a list.
        """,
    )
    active = models.BooleanField(
        help_text="Do you want the field to be visable on your form?",
        verbose_name="Is active?",
        default=True,
    )
    tags = TaggableManager()

    def __str__(self):
        """Default display value in unicode encoding."""
        return self.name

    class Meta:
        """Attributes about the data model and admin options."""

        ordering = ['ranking']


class UserFiles(models.Model):
    """User profile files."""

    user = models.OneToOneField(
        User, related_name='user_files', editable=False,
    )
    mugshot = models.FileField(
        "Photo",
        upload_to=partial(upload_to_path, 'Photo'),
        validators=PHOTO_VALIDATORS,
        max_length=768,
        null=True,
        blank=True,
        help_text="JPEG format (.jpg)",
    )
    biography = models.FileField(
        upload_to=partial(upload_to_path, 'Bio'),
        validators=FILE_VALIDATORS,
        max_length=768,
        null=True,
        blank=True,
        help_text="PDF format",
    )
    media_release = models.FileField(
        upload_to=partial(upload_to_path, 'Media_Release'),
        validators=FILE_VALIDATORS,
        max_length=768,
        null=True,
        blank=True,
        help_text="""
            Media release forms may contain a handwritten or digital signature.
            File must be in PDF format.
        """,
    )
    irs_w9 = models.FileField(
        "IRS W9",
        upload_to=partial(upload_to_path, 'W9'),
        validators=FILE_VALIDATORS,
        max_length=768,
        null=True,
        blank=True,
        help_text="PDF format",
    )

    class Meta:
        """Attributes about the data model and admin options."""

        db_table = 'core_userfiles'

    def get_file_path(self):
        """Return the path prefix for the file."""
        return 'files'

    def get_slug(self):
        """Return the slug for this object class."""
        return 'users'

    def get_file_name(self):
        """Return the file name based on the user's name."""
        return '{0}.{1}'.format(
            self.user.last_name, self.user.first_name,
        )

    def get_file_timestamp(self, field):
        """Return the timestamp for the phile. i.e. when it was created."""
        return _timestamp(self, field)

    def status(self, field):
        """Determine if the file was uploaded before the deadline date."""
        timestamp = self.get_file_timestamp(field)
        stat = True
        if timestamp < get_start_date():
            stat = False
        return stat

    def __str__(self):
        """Default display value in unicode encoding."""
        return 'User Profile File'


class UserProfile(models.Model):
    """User profile for the django user class."""

    # meta
    user = models.OneToOneField(User, related_name='profile')
    updated_by = models.ForeignKey(
        User,
        verbose_name="Updated by",
        related_name='user_profile_updated_by',
        editable=False,
    )
    date_created = models.DateTimeField("Date Created", auto_now_add=True)
    date_updated = models.DateTimeField("Date Updated", auto_now=True)
    # core
    salutation = models.CharField(
        max_length=16,
        choices=SALUTATION_TITLES,
        null=True,
        blank=True,
    )
    second_name = models.CharField(
        max_length=30,
        null=True,
        blank=True,
    )
    address1 = models.CharField("Address", max_length=128)
    address2 = models.CharField("", max_length=128, null=True, blank=True)
    city = models.CharField("City", max_length=128)
    state = models.CharField("State", max_length=2, choices=STATE_CHOICES)
    postal_code = models.CharField("Zip code", max_length=10)
    address1_current = models.CharField(
        "Address",
        max_length=128,
        null=True,
        blank=True,
    )
    address2_current = models.CharField("", max_length=128, null=True, blank=True)
    city_current = models.CharField("City", max_length=128, null=True, blank=True)
    state_current = models.CharField(
        "State",
        max_length=2,
        choices=STATE_CHOICES,
        null=True,
        blank=True,
    )
    postal_code_current = models.CharField(
        "Zip code",
        max_length=10,
        null=True,
        blank=True,
    )
    phone_primary = models.CharField(
        verbose_name='Primary phone',
        max_length=12,
        help_text="Format: XXX-XXX-XXXX",
    )
    phone_mobile = models.CharField(
        verbose_name='Cell phone',
        max_length=12,
        help_text="Format: XXX-XXX-XXXX",
        null=True,
        blank=True,
    )
    date_of_birth = models.DateField(
        "Date of birth", help_text="Format: mm/dd/yyyy",
    )
    gender = models.CharField(max_length=16, choices=GENDER_CHOICES)
    race = models.ManyToManyField(
        GenericChoice,
        related_name="user_profile_race",
        help_text='Check all that apply',
    )
    tribe = models.CharField("Tribe", max_length=128, null=True, blank=True)
    disability = models.CharField(
        "Disability status",
        max_length=64,
        choices=DISABILITY_CHOICES,
    )
    disability_specify = models.CharField(
        "Specify if not listed",
        max_length=255,
        null=True,
        blank=True,
    )
    us_citizen = models.CharField(
        "United States Citizen",
        max_length=4,
        choices=BINARY_CHOICES,
    )
    employment = models.CharField(
        "Employment status",
        max_length=128,
        choices=EMPLOYMENT_CHOICES,
    )
    military = models.CharField(
        "Have you served in the United States military?",
        max_length=4,
        choices=BINARY_CHOICES,
    )
    registration_type = models.CharField(
        max_length=32,
        choices=REG_TYPE,
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
        'application.WomenInAviationScholarship',
        'application.UndergraduateResearch',
        'application.UndergraduateScholarship',
        'application.NasaCompetition',
        'application.IndustryInternship',
        'application.ProfessionalProgramStudent',
    )

    class Meta:
        """Attributes about the data model and admin options."""

        db_table = 'core_userprofile'

    def __str__(self):
        """Default display value in unicode encoding."""
        return "{0} {1}'s profile".format(
            self.user.first_name, self.user.last_name,
        )

    def email_auxiliary(self):
        """Return the secondary email for the user."""
        return get_email_auxiliary(self.user)

    def get_race(self):
        """Return all of the race choices selected by the user."""
        race = ""
        for raza in self.race.all():
            race += "{0},".format(raza)
        return race[:-1]

    def get_registration(self):
        """Return registration relationship for the user."""
        # these imports need to be here, rather than at the top with the others
        import django
        from djspace.registration.models import Faculty
        from djspace.registration.models import Graduate
        from djspace.registration.models import GrantsOfficer
        from djspace.registration.models import HighSchool
        from djspace.registration.models import Professional
        from djspace.registration.models import Undergraduate

        if self.registration_type:
            mod = django.apps.apps.get_model(
                app_label='registration', model_name=self.registration_type,
            )
            return mod.objects.get(user=self.user)
        else:
            return None


@receiver(pre_save, sender=UserProfile)
def notify_administrators(sender, **kwargs):
    """Send an email to  WSGC administrators of registration update."""
    reggie = kwargs['instance']
    if reggie.pk is not None and not profile_status(reggie.user):
        registration_notify(kwargs.get('request'), 'update', reggie.user)


@receiver(user_signed_up, dispatch_uid='allauth.user_signed_up')
def _user_signed_up(request, user, **kwargs):
    """
    Dispatch ID needs to be unique for each signal handler, nothing more.

    As a result, We can use package plus signal name.
    """
    from allauth.account.models import EmailAddress
    # Add secondary email address for the user, and send email confirmation.
    # try/except for the rare cases when someone tries to register after they
    # have already done so and the email they are attempting to use somehow
    # slipped past our form clean() method.
    try:
        EmailAddress.objects.add_email(
            request, user, request.POST.get('email_secondary'), confirm=True,
        )
    except Exception:
        pass
    # create UserFiles() object for storing uploaded files after grant approval
    uf = UserFiles(user=user)
    uf.save()
    # notify WSGC administrators of new user registration
    registration_notify(request, 'create', user)
