# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import models, connection
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
    ('undergrad','Undergraduate'),
    ('graduate','Graduate'),
    ('professional','Professional'),
    ('professor','Professor'),
    ('k12educator','K12 Educator'),
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
    ("bachelor","Bachelor's degree"),
    ("associate","Associate's degree/certificate")
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

class BasePersonal(models.Model):

    salutation = models.CharField(
        "Salutation",
        max_length=10,
        choices=SALUTATION_TITLES
    )
    first = models.CharField(
        "First name",
        max_length=20
    )
    middle = models.CharField(
        "Middle initial",
        max_length=1
    )
    last = models.CharField(
        "Last name",
        max_length=20
    )
    citizen = models.BooleanField(
        '''Are you a U.S. citizen?
        U.S. citizenship is required
        for participation in WSGC programs.
        Non U.S. citizens are not
        eligible for WSGC funding.''',
        choices=BINARY_CHOICES
    )
    rocket_comp = models.BooleanField(
        '''Do you intend to apply for
        funding for the Tribal or AISES
        Rocket Competitions? Tribal or
        AISES Rocket Competition''',
        choices=BINARY_CHOICES
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
    address = models.CharField(
        "Mailing address",
        max_length=128
    )
    street = models.CharField(
        "Street",
        max_length=128,
        blank=True
    )
    city = models.CharField(
        "City",
        max_length=128,
        blank=True
    )
    state = models.CharField(
        "State",
        max_length=2,
        choices=STATE_CHOICES,
        blank=True
    )
    ZIP = models.CharField(
        "Zip code",
        max_length=9,
        blank=True
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
        max_length=128,
        choices=RACES
    )
    tribe = models.CharField(
        "Tribe",
        max_length=20,
        blank=True
    )


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
    employer_zip = models.CharField(
        "Employer zip code",
        max_length=9
    )


class BaseWSGC(models.Model):
    
    wsgc_school = models.CharField(
        "WSGC college enrolled or applied to",
        choices=WSGC_SCHOOL
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
        "WSGC advisor email",
        max_length=20
    )
    wsgc_advisor_confirm_email = models.EmailField(
        "WSGC advisor confirm email",
        max_length=20
    )
    wsgc_advisor_phone = models.CharField(
        "Phone number",
        max_length=16
    )
    
    
class BaseHighschool(models.Model):
    
    highschool_name = models.CharField(
        "Highschool name",
        max_length=20
    )
    highschool_street = models.CharField(
        "Highschool street",
        max_length=20
    )
    highschool_city = models.CharField(
        "Highschool city",
        max_length=20
    )
    highschool_state = models.CharField(
        "Highschool state",
        max_length=2,
        choices=STATE_CHOICES
    )
    highschool_zip = models.CharField(
        "Highschool zip code",
        max_length=9
    )
    
    
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
    gpa = models.FloatField(
        "Current cumulative GPA",
        max_length=4
    )
    gpa_major = models.FloatField(
        "GPA in major",
        max_length=4
    )
    scale = models.IntegerField(
        "GPA scale",
        max_length=1
    )
    CREDITS = models.FloatField(
        "Cumulative college credits",
        max_length=5
    )
    graduation = models.CharField(
        "Expected month and year of graduation",
        max_length=10
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

class BaseCollege(models.Model):
    
    university_street = models.CharField(
        "University street",
        max_length=128
    )
    university_city = models.CharField(
        "University city",
        max_length=128
    )
    university_state = models.CharField(
        "University state",
        max_length=2,
        choices=STATE_CHOICES
    )
    university_zip = models.CharField(
        "University zip code",
        max_length=9
    )
    undergraduate_degree = models.CharField(
        "Degree you are seeking",
        max_length=20,
        choices=UNDERGRADUATE_DEGREE
    )
