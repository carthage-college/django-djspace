# -*- coding: utf-8 -*-

from functools import partial

from django.db import models
from djspace.core.models import FILE_VALIDATORS
from djspace.core.models import Base
from djspace.core.models import GenericChoice
from djspace.core.utils import upload_to_path
from djspace.registration.choices import GRADUATE_DEGREE
from djspace.registration.choices import MAJORS
from djspace.registration.choices import UNDERGRADUATE_DEGREE
from djspace.registration.choices import YEAR_CHOICES
from djtools.fields import STATE_CHOICES
from djtools.fields.validators import credit_gpa_validator
from djtools.fields.validators import four_digit_year_validator


class BaseStudent(Base):
    """Abstract data model for all student registration types."""

    class Meta:
        """Attributes about the data model and admin options."""

        abstract = True

    # core
    major = models.CharField(
        "Primary major",
        max_length=128,
        choices=MAJORS,
    )
    major_other = models.CharField(
        "If other, please state",
        max_length=128,
        null=True,
        blank=True,
    )
    secondary_major_minor = models.CharField(
        "Secondary major or minor",
        max_length=128,
        null=True,
        blank=True,
        choices=MAJORS,
    )
    secondary_major_minor_other = models.CharField(
        "If other, please state",
        max_length=128,
        null=True,
        blank=True,
    )
    current_cumulative_gpa = models.CharField(
        "Current cumulative GPA",
        max_length=4,
        validators=[credit_gpa_validator],
    )
    gpa_in_major = models.CharField(
        "GPA in major",
        max_length=4,
    )
    gpa_scale = models.CharField(
        "GPA scale",
        max_length=4,
    )
    cumulative_college_credits = models.CharField(
        "Cumulative college credits", max_length=6,
    )
    month_year_of_graduation = models.CharField(
        "Expected month and year of graduation", max_length=7,
    )
    studentid = models.CharField(
        "Student ID Number", max_length=64,
    )
    wsgc_affiliate = models.ForeignKey(
        GenericChoice,
        verbose_name="College or University",
        related_name='student_wsgc_affiliate',
        max_length=128,
        on_delete=models.SET_NULL,
        null=True,
    )
    wsgc_affiliate_other = models.CharField(
        "Other",
        max_length=128,
        null=True,
        blank=True,
        help_text="""
            If your institution does not appear in the list above,
            please provide it here.
        """,
    )
    cv = models.FileField(
        "Résumé (optional)",
        upload_to=partial(upload_to_path, 'CV'),
        validators=FILE_VALIDATORS,
        max_length=768,
        null=True,
        blank=True,
        help_text="PDF format",
    )
    cv_authorize = models.BooleanField(
        """
            I authorize Wisconsin Space Grant Consortium to provide my résumé
            to Wisconsin companies seeking to place interns and co-ops.
        """,
    )

    def get_file_path(self):
        """Obtain the file path prefix."""
        return 'files'

    def get_slug(self):
        """Obtain the slug for the data model."""
        return 'users'

    def get_file_name(self):
        """Construct the file name."""
        return '{0}.{1}'.format(
            self.user.last_name, self.user.first_name,
        )


class HighSchool(Base):
    """High School student registration type."""

    name = models.CharField("School name", max_length=128)
    city = models.CharField("City", max_length=128)
    state = models.CharField("State", max_length=2, choices=STATE_CHOICES)
    major = models.CharField("Intended Major", max_length=128)
    gpa = models.CharField(
        "Cumulative GPA",
        max_length=4,
        validators=[credit_gpa_validator],
    )
    gpa_scale = models.CharField(
        "GPA Scale",
        max_length=4,
        validators=[credit_gpa_validator],
    )
    secondary_education = models.CharField(
        "College or University attending in the Fall", max_length=128,
    )
    student_identification = models.CharField(
        "College or University Student ID", max_length=32,
    )


class Undergraduate(BaseStudent):
    """Undergraduate student registration type."""

    wsgc_affiliate = models.ForeignKey(
        GenericChoice,
        verbose_name="College or University",
        related_name='undergrad_wsgc_affiliate',
        max_length=128,
        on_delete=models.SET_NULL,
        null=True,
    )
    highschool_name = models.CharField("High school name", max_length=128)
    highschool_city = models.CharField("High school city", max_length=128)
    highschool_state = models.CharField(
        "High school state",
        max_length=2,
        choices=STATE_CHOICES,
    )
    class_year = models.CharField(
        "Current Class Status",
        max_length=24,
        choices=YEAR_CHOICES,
    )


class Graduate(BaseStudent):
    """Graduate student registration type."""

    wsgc_affiliate = models.ForeignKey(
        GenericChoice,
        verbose_name="College or University",
        related_name='graduate_wsgc_affiliate',
        max_length=128,
        on_delete=models.SET_NULL,
        null=True,
    )
    undergraduate_degree = models.CharField(
        max_length=32,
        choices=UNDERGRADUATE_DEGREE,
    )
    degree_program = models.CharField(max_length=32, choices=GRADUATE_DEGREE)
    degree_program_other = models.CharField(
        "Other",
        max_length=128,
        null=True,
        blank=True,
    )
    concentration_area = models.CharField(
        "Concentration area (eg. physics, astronomy, physiology, etc.)",
        max_length=128,
    )
    graduate_gpa = models.CharField(
        "Current cumulative GPA",
        max_length=4,
        validators=[credit_gpa_validator],
    )
    graduate_scale = models.CharField(
        "GPA Scale",
        max_length=4,
        validators=[credit_gpa_validator],
    )
    graduate_graduation_year = models.CharField(
        "Anticipated graduation year",
        max_length=4,
        validators=[four_digit_year_validator],
    )


class Academic(Base):
    """Abstract data model base class for academics."""

    class Meta:
        """Attributes about the data model and admin options."""

        abstract = True

    # core
    wsgc_affiliate = models.ForeignKey(
        GenericChoice,
        verbose_name="Institution/Organization",
        on_delete=models.SET_NULL,
        null=True,
        help_text="""
            You must be associated with a WSGC commercial, government, or
            nonprofit affiliate in order to proceed
        """,
    )
    wsgc_affiliate_other = models.CharField(
        "Other",
        max_length=128,
        null=True,
        blank=True,
        help_text="""
            If your institution does not appear in the list above,
            please provide it here.
        """,
    )
    department_program = models.CharField("Department / Program", max_length=128)
    title = models.CharField(
        "Title (eg. Assistant Prof., Associate Prof., Prof.)",
        max_length=128,
    )


class Faculty(Academic):
    """Faculty registration type."""

    class Meta:
        """Attributes about the data model and admin options."""

        verbose_name_plural = "Faculty"


class GrantsOfficer(Academic):
    """Grants Officer registration type."""

    class Meta:
        """Attributes about the data model and admin options."""

        verbose_name_plural = "Authorized User"


class Professional(Base):
    """Professional registration type."""

    # core
    wsgc_affiliate = models.ForeignKey(
        GenericChoice,
        verbose_name="Institution/Organization",
        related_name='professional_wsgc_affiliate',
        on_delete=models.SET_NULL,
        null=True,
        help_text="""
            You must be associated with a WSGC commercial, government, or
            nonprofit affiliate in order to proceed
        """,
    )
    sponsoring_organization_name = models.CharField(
        "Name",
        max_length=128,
        null=True,
        blank=True,
    )
    sponsoring_organization_address1 = models.CharField(
        "Address",
        max_length=128,
        null=True,
        blank=True,
    )
    sponsoring_organization_address2 = models.CharField(
        "",
        max_length=128,
        null=True,
        blank=True,
    )
    sponsoring_organization_city = models.CharField(
        "City",
        max_length=128,
        null=True,
        blank=True,
    )
    sponsoring_organization_state = models.CharField(
        "State",
        max_length=2,
        choices=STATE_CHOICES,
        null=True,
        blank=True,
    )
    sponsoring_organization_postal_code = models.CharField(
        "Zip code",
        max_length=10,
        null=True,
        blank=True,
    )
    sponsoring_organization_contact = models.CharField(
        "Contact",
        max_length=128,
        null=True,
        blank=True,
    )
    sponsoring_organization_description = models.TextField(
        "Description",
        null=True,
        blank=True,
    )
