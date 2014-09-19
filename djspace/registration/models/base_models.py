# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import models, connection
from djspace.registration.validators import *
from django.contrib.auth.models import User

from djtools.fields import BINARY_CHOICES, SALUTATION_TITLES, STATE_CHOICES
from djtools.fields import GENDER_CHOICES

YES_NO_DECLINE = (
    ('Yes', 'Yes'),
    ('No', 'No'),
    ('Decline', 'Decline to state')
)

RACES = (
    ('American Indian/Alaska Native','American Indian/Alaska Native'),
    ('Asian','Asian'),
    ('Black/African American','Black/African American'),
    ('Caucasian','Caucasian'),
    ('Hispanic','Hispanic'),
    ('Native Hawaiian/Other Pacific Islander','Native Hawaiian/Other Pacific Islander'),
    ('Other','Other')
)

'''
REMOVE THIS
DON'T NEED IT ANYMORE  -ZW

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
)'''

GRADUATE_DEGREE = (
    ('M.S.','M.S.'),
    ('Ph.D','Ph.D'),
    ('M.D.','M.D.'),
    ('Other','Other')
)

EMPLOYER = (
    ('sad','OH NO, WE NEED TO FILL THESE OUT'),
    ('stillsad','Still sad')
)

WSGC_SCHOOL = (
    ('alverno','Alverno College'),
    ('carroll','Carroll University'),
    ('carthage','Carthage College'),
    ('menominee','College of Menominee Nation'),
    ('lawrence','Lawrence University'),
    ('marquette','Marquette University'),
    ('medicalwisconsin','Medical College of Wisconsin'),
    ('msoe','Milwaukee School of Engineering'),
    ('ripon','Ripon College'),
    ('stnorbert','St. Norbert College'),
    ('uwfoxvalley','UW Fox Valley'),
    ('uwgreenbay','UW Green Bay'),
    ('uwlacrosse','UW LaCrosse'),
    ('uwmadison','UW Madison'),
    ('uwmilwaukee','UW Milwaukee'),
    ('uwoshkosh','UW Oshkosh'),
    ('uwparkside','UW Parkside'),
    ('uwplatteville','UW Platteville'),
    ('uwriverfalls','UW River Falls'),
    ('uwstephenspoint','UW Stevens Point'),
    ('uwstout','UW Stout'),
    ('uwsuperior','UW Superior'),
    ('uwshitewater','UW Whitewater'),
    ('westerntechnical','Western Technical College'),
    ('wisconsinlutheran','Wisconsin Lutheran College')
)

WSGC_AFFILIATE = (
    ('Aerogel Technolgies','Aerogel Technolgies'),
    ('Astronautics','Astronautics'),
    ('BTCI','BTCI'),
    ('Charter','Charter'),
    ('Crossroads at Big Creek','Crossroads at Big Creek'),
    ('DOT','DOT'),
    ('DPI','DPI'),
    ('EAA','EAA'), 
    ('Orbitec','Orbitec'),
    ('Space Explorers','Space Explorers'),
    ('Space Port','Space Port'),
    ('Sheboygan', 'Sheboygan'),
    ('StaatsQuest','StaatsQuest')
)

class BasePersonal(models.Model):

    salutation = models.CharField(
        "Salutation",
        max_length=16,
        null=True, blank=True
    )
    first_name = models.CharField(
        "First name",
        max_length=128
    )
    middle_initial = models.CharField(
        "Middle initial",
        max_length=1
    )
    last_name = models.CharField(
        "Last name",
        max_length=128
    )    
    address_1 = models.CharField(
        "Address line 1",
        max_length=128
    )
    address_2 = models.CharField(
        "Address line 2",
        max_length=128,
        blank=True
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
    email = models.EmailField(
        "Email"
    )
    disability = models.CharField(
        "Disability status",
        max_length=16,
        choices=YES_NO_DECLINE
    )
    tribe = models.CharField(
        "Tribe",
        max_length=128,
        blank=True
    )

    class Meta:
        abstract = True
        

class BaseWSGC(models.Model):

    wsgc_school = models.CharField(
        "WSGC College or University applied to",
        choices=WSGC_SCHOOL,
        max_length=128
    )

    class Meta:
        abstract = True


class BaseUndergrad(models.Model):

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

    class Meta:
        abstract = True
