# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import models, connection
from django.core.validators import *
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

PROFESSION = (
    ('Undergrad','Undergraduate'),
    ('Graduate','Graduate'),
    ('Professional','Professional'),
    ('Professor','Professor'),
    ('K12 Educator','K12 Educator'),
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


UNDERGRADUATE_DEGREE = (
    ("Bachelor's degree","Bachelor's degree"),
    ("Associate's degree/certificate","Associate's degree/certificate")
)

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
        max_length=10,
        null=True, blank=True
    )
    first = models.CharField(
        "First name",
        max_length=128
    )
    middle = models.CharField(
        "Middle initial",
        max_length=1
    )
    last = models.CharField(
        "Last name",
        max_length=128
    )
    citizen = models.CharField(
        '''Are you a U.S. citizen?
        U.S. citizenship is required
        for participation in WSGC programs.
        Non U.S. citizens are not
        eligible for WSGC funding.''',
        choices=BINARY_CHOICES,
        max_length=4
    )
    maiden = models.CharField(
        "Maiden name",
        max_length=20
    )
    additional = models.CharField(
        "Additional name",
        max_length=20
    )
    department_program = models.CharField(
        "Department / Program",
        max_length=128
    )
    title = models.CharField(
        "Title (eg. Assistant Prof., Associate Prof., Prof.)",
        max_length=128
    )
    webpage = models.CharField(
        "Web page",
        max_length=128,
        blank=True
    )
    address = models.CharField(
        "Mailing address",
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
    street = models.CharField(
        "Street",
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
    phone = models.CharField(
        "Phone number",
        max_length=16
    )
    primary = models.CharField(
        "Primary interest",
        max_length=35,
        choices=INTEREST
    )
    email = models.EmailField(
        "Email"
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
    #birthdate = models.DateField(
    #    "Birthdate",
    #    auto_now=False
    #)
    gender = models.CharField(
        "Gender",
        max_length=24,
        choices=GENDER_CHOICES
    )
    disability = models.CharField(
        "Disability status",
        max_length=16,
        choices=YES_NO_DECLINE
    )
    race = models.CharField(
        "Race",
        max_length=128
    )
    tribe = models.CharField(
        "Tribe",
        max_length=20,
        blank=True
    )

    class Meta:
        abstract = True


class BaseEmployer(models.Model):

    employer = models.CharField(
        "Employer",
        max_length=20,
        choices=EMPLOYER
    )
    employer_name = models.CharField(
        "Employer name",
        max_length=20,
        choices=EMPLOYER
    )
    employer_street = models.CharField(
        "Employer street",
        max_length=20
    )
    employer_city = models.CharField(
        "Employer city",
        max_length=20
    )
    employer_state = models.CharField(
        "Employer state",
        max_length=2,
        choices=STATE_CHOICES
    )
    employer_postal_code = models.CharField(
        "Employer zip code",
        max_length=9
    )


class BaseWSGC(models.Model):

    wsgc_school = models.CharField(
        "WSGC College or University applied to",
        choices=WSGC_SCHOOL,
        max_length=128
    )
    wsgc_school_num = models.CharField(
        "WSGC college enrolled or applied to student number",
        max_length=20
    )
    wsgc_advisor_salutation = models.CharField(
        "WSGC advisor salutation",
        max_length=10,
        choices=SALUTATION_TITLES
    )
    wsgc_advisor_first = models.CharField(
        "WSGC advisor first name",
        max_length=20
    )
    wsgc_advisor_middle = models.CharField(
        "WSGC advisor middle name",
        max_length=20
    )
    wsgc_advisor_last = models.CharField(
        "WSGC advisor last name",
        max_length=20
    )
    wsgc_advisor_title_department = models.CharField(
        "WSGC advisor title or department",
        max_length=20
    )
    wsgc_advisor_email = models.EmailField(
        "WSGC advisor email"
    )
    wsgc_advisor_confirm_email = models.EmailField(
        "WSGC advisor confirm email"
    )
    wsgc_advisor_phone = models.CharField(
        "Phone number",
        max_length=16
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
    gpa = models.CharField(
        "Current cumulative GPA",
        max_length=4,
        validators=[credit_gpa_validator]
    )
    gpa_major = models.CharField(
        "GPA in major",
        max_length=4,
        validators=[credit_gpa_validator]
    )
    scale = models.CharField(
        "GPA scale",
        max_length=4,
        validators=[credit_gpa_validator]
    )
    CREDITS = models.CharField(
        "Cumulative college credits",
        max_length=6,
        validators=[credit_gpa_validator]
    )
    graduation = models.CharField(
        "Expected month and year of graduation",
        max_length=7,
        validators=[month_year_validator]
    )
    #degree = models.CharField(
    #   "Degree you are seeking",
    #    max_length=20,
    #    choices=UNDERGRADUATE_DEGREE
    #)
    campus_mailing = models.CharField(
        "Campus mailing address",
        max_length=128
    )

    class Meta:
        abstract = True
