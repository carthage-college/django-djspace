# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import models, connection
from django.contrib.auth.models import User
from djspace.registration.base_models import *

from djtools.fields import BINARY_CHOICES, SALUTATION_TITLES, STATE_CHOICES
from djtools.fields import GENDER_CHOICES


EMPLOYER = (
    (':\(','OH NO, WE NEED TO FILL THESE OUT')    
)

INTEREST = (
    ('aeronauticalaerospace','Aeronautical/Aerospace'),
    ('agricultural','Agricultural'),
    ('anthropology','Anthropology'),
    ('architectural','Architectural'),
    ('architecture','Architecture'),
    ('art','Art'),
    ('astronomy','Astronomy'),
    ('astrophysics','Astrophysics'),
    ('atmosphericscience','Atmospheric Science'),
    ('biochemistry','Biochemistry'),
    ('bioengineering','Bioengineering'),
    ('biology','Biology'),
    ('botany','Botany'),
    ('chemical','Chemistry'),
    ('civil','Civil'),
    ('climatologymeteorology','Climatology/Meteorology'),
    ('computer','Computer'),
    ('computerscience','Computer Science'),
    ('earthsciences','Earth Sciences'),
    ('economics','Economics'),
    ('educationelementaryschool','Elementary Education School'),
    ('educationhighschool','Education High School'),
    ('educationk12','Education K12'),
    ('educationk12administration','Education K12 Administration'),
    ('educationmiddleschool','Education Middle School'),
    ('electricalelectronic','Electrical/Electronic'),
    ('engineering','Engineering'),
    ('engineeringmechanics','Engineering Mechanics'),
    ('engineeringscience','Engineering Science'),
    ('environmental','Environmental'),
    ('environmentalscience','Environmental Science'),
    ('environmentalscienceandglobalclimatechange','Environmental and Global Climate Change'),
    ('generalpublic','General Public'),
    ('geography','Geography'),
    ('geology','Geology'),
    ('geophysics','Geophysics'),
    ('healthsciencenutrition','Health Science/Nutrition'),
    ('history','History'),
    ('industrial','Industrial'),
    ('lifesciences','Life Sciences'),
    ('materialsscienceengineering','Materials Science'),
    ('mathematics','Mathematics'),
    ('mechanical','Mechanical'),
    ('medicinemedicalresearch','Medicine/Medical Research'),
    ('miningpetroleumnaturalgas','Mining/Petroleum and Natural Gas'),
    ('molecularcellbiology','Molecular/Cell Biology'),
    ('nuclear','Nuclear'),
    ('oceanography','Oceanography'),
    ('other','Other'),
    ('philosophy','Philosophy'),
    ('physicalscience','Physical Science'),
    ('physics','Physics'),
    ('planetarygeosciences','Planetary GeoSciences'),
    ('planetarysciences','Planetary Sciences'),
    ('politicalsciencepublicpolicy','Political Science/Public Policy'),
    ('psychology','Psychology'),
    ('socialsciences','Social Sciences'),
    ('sociology','Sociology'),
    ('zoology','Zoology')
)

RACE = (
    ('americanindianalaskanative','American Indian/Alaska Native'),
    ('asian','Asian'),
    ('blackafricanamerican','Black/African American'),
    ('caucasian','Caucasian'),
    ('hispanic','Hispanic'),
    ('nativehawaiianotherpacificislander','Native Hawaiian/Other Pacific Islander'),
    ('otherrace','Other race')
)




class ProfessorInformation(BasePersonalInformation,BaseEmployerInformation):
    
    first = models.CharField(
        "First name",
        max_length=20
    )
    middle = models.CharField(
        "Middle name",
        max_length=20
    )
    last = models.CharField(
        "Last name",
        max_length=20
    )
    citizen = models.BooleanField(
        "US Citizen"
    )
    rocket_comp = models.BooleanField(
        "Tribal or AISES Rocket Competition"
    )
    maiden = models.CharField(
        "Maiden name",
        max_length=20
    )
    additional = models.CharField(
        "Additional name",
        max_length=20
    )
    title_department = models.CharField(
        "Title or Department",
        max_length=20
    )
    webpage = models.CharField(
        "Web page",
        max_length=20
    )
    street = models.CharField(
        "Street",
        max_length=20
    )
    city = models.CharField(
        "City",
        max_length=20
    )
    state = models.CharField(
        "State",
        max_length=2,
        choices=STATE_CHOICES
    )
    ZIP = models.CharField(
        "Zip code",
        max_length=9
    )
    phone = models.CharField(
        "Phone number",
        max_length=16
    )
    primary = models.CharField(
        "Primary interest",
        max_length=35,
        choices=INTEREST
    )
    primary_other = models.CharField(
        "Other",
        max_length=35
    )
    secondary = models.CharField(
        "Secondary interest",
        max_length=35,
        choices=INTEREST
    )
    secondary_other = models.CharField(
        "Other",
        max_length=35
    )
    birthdate = models.DateField(
        "Birthdate",
        auto_now=False
    )
    gender = models.CharField(
        "Gender",
        max_length=8,
        choices=GENDER_CHOICES
    )
    disability = models.BooleanField(
        "Disability"
    )
    race = models.CharField(
        "Race",
        max_length=25,
        choices=RACE
    )
    tribe = models.CharField(
        "Tribe",
        max_length=20
    )
