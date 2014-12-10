# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

from djspace.registration.choices import WSGC_SCHOOL, MAJORS
from djspace.registration.choices import UNDERGRADUATE_DEGREE, GRADUATE_DEGREE
from djspace.core.models import BaseModel, GenericChoice

from djtools.fields import STATE_CHOICES
from djtools.fields.validators import *

def limit_affiliation():
    ids = [
        g.id for g in GenericChoice.objects.filter(
            tags__name__in=["WSGC Affiliates"]
        ).order_by("name")
    ]
    return ids

def limit_college_university():
    ids = [
        g.id for g in GenericChoice.objects.filter(
            tags__name__in=["College or University"]
        ).order_by("name")
    ]
    return ids

def limit_generic_choice(tag):
    """
    why does this not work?
    """
    ids = [
        g.id for g in GenericChoice.objects.filter(
            tags__name__in=[tag]
        ).order_by("name")
    ]
    return ids


class BaseStudent(BaseModel):

    # core
    major = models.CharField(
        "Primary major",
        max_length=128,
        choices=MAJORS
    )
    major_other = models.CharField(
        "If Other, please state",
        max_length=128,
        null=True, blank=True
    )
    secondary_major_minor = models.CharField(
        "Secondary major or minor",
        max_length=128,
        null=True, blank=True,
        choices=MAJORS
    )
    secondary_major_minor_other = models.CharField(
        "If Other, please state",
        max_length=128,
        null=True, blank=True
    )
    current_cumulative_gpa = models.CharField(
        "Current cumulative GPA",
        max_length=4,
        validators=[credit_gpa_validator]
    )
    gpa_in_major = models.CharField(
        "GPA in major",
        max_length=4,
        validators=[credit_gpa_validator]
    )
    gpa_scale = models.CharField(
        "GPA scale",
        max_length=4,
        validators=[credit_gpa_validator]
    )
    cumulative_college_credits = models.CharField(
        "Cumulative college credits",
        max_length=6,
        validators=[credit_gpa_validator]
    )
    month_year_of_graduation = models.CharField(
        "Expected month and year of graduation",
        max_length=7,
        validators=[month_year_validator]
    )
    wsgc_school = models.ForeignKey(
        GenericChoice,
        verbose_name="College or University",
        limit_choices_to={"id__in":limit_college_university},
        #limit_choices_to={"id__in":limit_generic_choice("College or University")},
        help_text="FNL Participants: Choose 'OTHER.'",
        max_length=128
    )

    class Meta:
        abstract = True

class Undergraduate(BaseStudent):
    highschool_name = models.CharField(
        "High school name",
        max_length=128
    )
    highschool_city = models.CharField(
        "High school city",
        max_length=128
    )
    highschool_state = models.CharField(
        "High school state",
        max_length=2,
        choices=STATE_CHOICES
    )


class Graduate(BaseStudent):
    undergraduate_degree = models.CharField(
        max_length=32,
        choices=UNDERGRADUATE_DEGREE
    )
    degree_program = models.CharField(
        max_length=32,
        choices=GRADUATE_DEGREE
    )
    degree_program_other = models.CharField(
        "Other",
        max_length=128,
        null=True, blank=True,
    )
    concentration_area = models.CharField(
        "Concentration area (eg. physics, astronomy, physiology, etc.)",
        max_length=128
    )
    graduate_gpa = models.CharField(
        "Current cumulative GPA",
        max_length=4,
        validators=[credit_gpa_validator]
    )
    graduate_scale = models.CharField(
        "GPA Scale",
        max_length=4,
        validators=[credit_gpa_validator]
    )
    graduate_graduation_year = models.CharField(
        "Anticipated graduation year",
        max_length=4,
        validators=[four_digit_year_validator]
    )


class Faculty(BaseModel):

    # core
    department_program = models.CharField(
        "Department / Program",
        max_length=128
    )
    title = models.CharField(
        "Title (eg. Assistant Prof., Associate Prof., Prof.)",
        max_length=128
    )
    web_site = models.CharField(
        "Web site",
        max_length=128,
        help_text = "eg. www.mywebsite.com",
        null=True, blank=True,
    )

    class Meta:
        verbose_name_plural = "Faculty"


class Professional(BaseModel):

    # core
    wsgc_affiliate = models.ForeignKey(
        GenericChoice,
        limit_choices_to={"id__in":limit_affiliation},
        verbose_name="WSGC Affiliate",
        related_name="professional_wsgc_affiliate",
        on_delete=models.SET_NULL,
        null=True,
        help_text = """
            You must be associated with a WSGC commercial, government, or
            nonprofit affiliate in order to proceed
        """
    )
