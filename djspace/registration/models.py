# -*- coding: utf-8 -*-
from django.db import models

from djspace.registration.choices import WSGC_AFFILIATE, WSGC_SCHOOL
from djspace.registration.validators import *

from djtools.fields import STATE_CHOICES

class BaseStudent(models.Model):

    # NEEDS TO BE A DROP DOWN
    major = models.CharField(
        "Primary major",
        max_length=20
    )
    major_other = models.CharField(
        "Other",
        max_length=128,
        blank=True
    )
    # NEEDS TO BE A DROP DOWN
    secondary_major_minor = models.CharField(
        "Secondary major or minor",
        max_length=128
    )
    secondary_major_minor_other = models.CharField(
        "Other",
        max_length=128,
        blank=True
    )
    student_id = models.CharField(
        "Student ID",
        max_length=7
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
    wsgc_school = models.CharField(
        "WSGC College or University applied to",
        choices=WSGC_SCHOOL,
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

    degree_program_other = models.CharField(
        "Other",
        max_length=128,
        blank=True
    )
    concentration_area = models.CharField(
        "Concentration area (eg. physics, astronomy, physiology, etc.)",
        max_length=128
    )
    graduate_gpa = models.FloatField(
        "Current cumulative GPA",
        max_length=4,
        validators=[credit_gpa_validator]
    )
    graduate_scale = models.IntegerField(
        "GPA Scale",
        max_length=4,
        validators=[credit_gpa_validator]
    )
    graduate_graduation_year = models.CharField(
        "Anticipated graduation year",
        max_length=4,
        validators=[four_digit_year_validator]
    )


class Faculty(models.Model):

    campus_email = models.EmailField(
        "Campus email address"
    )
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
        blank=True
    )


#class K12Educator(models.Model):
#    pass


class Professional(models.Model):

    wsgc_affiliate = models.CharField(
        "WSGC Affiliate",
        max_length=128,
        choices=WSGC_AFFILIATE
    )
