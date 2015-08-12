# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.contrib.auth.models import User
from allauth.account.signals import user_signed_up
from allauth.account.models import EmailAddress

from djtools.fields import BINARY_CHOICES, YES_NO_DECLINE, STATE_CHOICES
from djtools.fields import GENDER_CHOICES, SALUTATION_TITLES
from djtools.utils.mail import send_mail

from taggit.managers import TaggableManager
from gm2m import GM2MField

from datetime import date

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

class Base(models.Model):

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
        max_length=3,
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
        max_length=9
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
        max_length=9,
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
        limit_choices_to={"id__in":limit_race},
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
    applications = GM2MField()


    def __unicode__(self):
        return u"{} {}'s profile".format(
            self.user.first_name, self.user.last_name
        )

    def get_registration(self):
        # these imports need to be here, rather than at the top with the others
        from djspace.registration.models import Undergraduate, Graduate
        from djspace.registration.models import Faculty, Professional

        try:
            return eval(self.registration_type).objects.get(user=self.user)
        except:
            return None

# dispatch ID needs to be unique for each signal handler, nothing more.
# so we can use package plus signal name.
@receiver(user_signed_up, dispatch_uid="allauth.user_signed_up")
def _user_signed_up(request, user, **kwargs):

    # Add secondary email address for the user, and send email confirmation.
    EmailAddress.objects.add_email(
        request, user, request.POST.get("email_secondary"), confirm=False
    )

    # notify WSGC administrators of new user registration
    subject = u"[WSGC Registration] {}, {}".format(
        user.last_name, user.first_name
    )
    if settings.DEBUG:
        TO_LIST = [settings.ADMINS[0][1],]
    else:
        TO_LIST = [settings.WSGC_APPLICATIONS,]
    template = "account/registration_alert_email.html"
    send_mail(
        request, TO_LIST,
        subject, user.email,
        template, {"user":user}, settings.MANAGERS
    )

