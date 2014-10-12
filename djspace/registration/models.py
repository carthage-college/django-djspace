# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

from djspace.registration.choices import WSGC_AFFILIATE, WSGC_SCHOOL
from djspace.registration.validators import *

from djtools.fields import STATE_CHOICES

MAJORS = (
    ('Aeronautical Engineering','Aeronautical Engineering'),
    ('Aerospace Engineering','Aerospace Engineering'),
    ('Applied Physics','Applied Physics'),
    ('Astronomy','Astronomy'),
    ('Astrophysics','Astrophysics'),
    ('Atmoshperic Sciences','Atmoshperic Sciences'),
    ('Biochemistry','Biochemistry'),
    ('Biology','Biology'),
    ('Biomedical Engineering','Biomedical Engineering'),
    ('Biomedical Science','Biomedical Science'),
    ('Biophysics','Biophysics'),
    ('Biotechnology','Biotechnology'),
    ('Chemical Engineering','Chemical Engineering'),
    ('Chemistry','Chemistry'),
    ('Civil Engineering','Civil Engineering'),
    ('Computer Engineering','Computer Engineering'),
    ('Computer Science','Computer Science'),
    ('Electrical Engineering','Electrical Engineering'),
    ('Environmental Science','Environmental Science'),
    ('Environmental Studies','Environmental Studies'),
    ('Geography','Geography'),
    ('Geology','Geology'),
    ('Geophysics','Geophysics'),
    ('Geoscience','Geoscience'),
    ('Industrial Engineering','Industrial Engineering'),
    ('Kinesiology','Kinesiology'),
    ('Mathematics','Mathematics'),
    ('Mechanical Engineering','Mechanical Engineering'),
    ('Meteorology','Meteorology'),
    ('Microbiology','Microbiology'),
    ('Molecular and Cell Biology','Molecular and Cell Biology'),
    ('Molecular and Environmental Plant Science','Molecular and Environmental Plant Science'),
    ('Neuroscience','Neuroscience'),
    ('Nuclear Engineering','Nuclear Engineering'),
    ('Oceanography','Oceanography'),
    ('Other','Other'),
    ('Physics','Physics'),
    ('Statistics','Statistics'),
    ('Systems Engineering','Systems Engineering')
)


class BaseStudent(models.Model):

    # Django user
    user = models.ForeignKey(User)
    # NEEDS TO BE A DROP DOWN
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
    # NEEDS TO BE A DROP DOWN
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
        "WSGC College or University",
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

    degree_program = models.CharField(
        max_length=32,
        null=True, blank=True,
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


class Faculty(models.Model):

    # Django user
    user = models.ForeignKey(User)
    # etc
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
        null=True, blank=True,
    )


class Professional(models.Model):

    # Django user
    user = models.ForeignKey(User)
    # etc
    wsgc_affiliate = models.CharField(
        "WSGC Affiliate",
        max_length=128,
        help_text = """
            You must be associated with a WSGC commercial, government, or
            nonprofit affiliate in order to proceed
        """,
        choices=WSGC_AFFILIATE
    )
