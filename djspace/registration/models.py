# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import models, connection
from django.contrib.auth.models import User

from djtools.fields import BINARY_CHOICES, SALUTATION_TITLES, STATE_CHOICES
from djtools.fields import GENDER_CHOICES

UNDERGRADUATE_DEGREE = (
    ('associate','Associates'),
    ('bachelor','Bachelors')
)

GRADUATE_DEGREE = (
    ('master','Masters'),
    ('doctorate','Doctorate'),
    ('other','Other')
)

PROFESSION = (
    ('undergrad','Undergraduate'),
    ('graduate','Graduate'),
    ('professional','Professional'),
    ('professor','Professor'),
    ('k12educator','K12 Educator'),
)

PRIMARY_INTEREST = (
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

SECONDARY_INTEREST = (
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


class UndergraduateInformation():

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
        choices=PRIMARY_INTEREST
    )
    primary_other = models.CharField(
        "Other",
        max_length=35
    )
    secondary = models.CharField(
        "Secondary interest",
        max_length=35,
        choices=SECONDARY_INTEREST
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
    wsgc_school = models.CharField(
        "WSGC college enrolled or applied to",
        max_length=20
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
    degree_seeking = models.CharField(
        "Degree seeking",
        max_length=20,
        choices=PROFESSION
    )
    ultimate_degree_seeking = models.CharField(
        "Ultimate degree seeking",
        max_length=20,
        choices=PROFESSION
    )
    # Going to need select options later
    major = models.CharField(
        "Major",
        max_length=20
    )
    # Going to need select options later
    major_2 = models.CharField(
        "Major 2",
        max_length=20
    )
    # Going to need select options later
    minor = models.CharField(
        "Minor",
        max_length=20
    )
    sat_verbal = models.IntegerField(
        "SAT Verbal",
        max_length=4
    )
    sat_math = models.IntegerField(
        "SAT Math",
        max_length=4
    )
    sat_total = models.IntegerField(
        "SAT Total",
        max_length=4
    )
    act_english = models.IntegerField(
        "ACT English",
        max_length=2
    )
    act_math = models.IntegerField(
        "ACT Math",
        max_length=2
    )
    act_reading = models.IntegerField(
        "ACT Reading",
        max_length=2
    )
    act_science = models.IntegerField(
        "ACT Science",
        max_length=2
    )
    act_composite = models.IntegerField(
        "ACT Composite",
        max_length=2
    )
    gpa = models.FloatField(
        "Current cumulative GPA",
        max_length=4
    )
    gpa_major = models.FloatField(
        "Major GPA",
        max_length=4
    )
    scale = models.IntegerField(
        "Scale",
        max_length=1
    )
    CREDITS = models.FloatField(
        "Credits",
        max_length=5
    )
    year_in_school = models.IntegerField(
        "Year in school as of next fall",
        max_length=4
    )
    graduation = models.DateField(
        "Expected date of graduation",
        auto_now=False
    )
    undergraduate_concentration = models.CharField(
        "Area of Undergraduate Concentration in a Space, Aerospace, or Space-Related Field",
        max_length=20
    )


class GraduateInformation(BasePersonalInformation):

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
        choices=PRIMARY_INTEREST
    )
    primary_other = models.CharField(
        "Other",
        max_length=35
    )
    secondary = models.CharField(
        "Secondary interest",
        max_length=35,
        choices=SECONDARY_INTEREST
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
        "Zip code",
        max_length=9
    )
    wsgc_school = models.CharField(
        "WSGC college enrolled or applied to",
        max_length=20
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
    university_name = models.CharField(
        "University name",
        max_length=20
    )
    university_street = models.CharField(
        "University street",
        max_length=20
    )
    university_city = models.CharField(
        "University city",
        max_length=20
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
        "University degree",
        max_length=20,
        choices=UNDERGRADUATE_DEGREE
    )
    # Going to need select options later
    major = models.CharField(
        "Major",
        max_length=20
    )
    # Going to need select options later
    major_2 = models.CharField(
        "Major 2",
        max_length=20
    )
    # Going to need select options later
    minor = models.CharField(
        "Minor",
        max_length=20
    )
    gpa = models.FloatField(
        "Current cumulative GPA",
        max_length=4
    )
    scale = models.IntegerField(
        "Scale",
        max_length=1
    )
    CREDITS = models.FloatField(
        "Credits",
        max_length=5
    )
    undergraduate_honors = models.CharField(
        "Undergraduate honors",
        max_length=20
    )
    graduation = models.DateField(
        "Graduation date",
        auto_now=False
    )
    gre_verbal = models.IntegerField(
        "GRE Verbal",
        max_length=3
    )
    gre_quantitative = models.IntegerField(
        "GRE Quantitative",
        max_length=3
    )
    gre_analytic = models.IntegerField(
        "GRE Analytic",
        max_length=3
    )
    test = models.CharField(
        "Other test",
        max_length=20
    )
    test_score = models.CharField(
        "Score",
        max_length=10
    )
    degree_seeking = models.CharField(
        "Degree seeking",
        max_length=20,
        choices=GRADUATE_DEGREE
    )
    ultimate_degree_seeking = models.CharField(
        "Ultimate degree seeking",
        max_length=20,
        choices=GRADUATE_DEGREE
    )
    # Going to need select options later
    graduate_major = models.CharField(
        "Major",
        max_length=20
    )
    graduate_emphasis = models.CharField(
        "Emphasis",
        max_length=20
    )
    gpa = models.FloatField(
        "Current cumulative GPA",
        max_length=4
    )
    gpa_major = models.FloatField(
        "Major GPA",
        max_length=4
    )
    scale = models.IntegerField(
        "Scale",
        max_length=1
    )
    CREDITS = models.FloatField(
        "Credits",
        max_length=5
    )
    year_in_school = models.IntegerField(
        "Year in school as of next fall",
        max_length=4
    )
    graduation = models.DateField(
        "Expected date of graduation",
        auto_now=False
    )
    

class ProfessionalInformation(BasePersonalInformation,BaseEmployerInformation):
    
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
        choices=PRIMARY_INTEREST
    )
    primary_other = models.CharField(
        "Other",
        max_length=35
    )
    secondary = models.CharField(
        "Secondary interest",
        max_length=35,
        choices=SECONDARY_INTEREST
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
        choices=PRIMARY_INTEREST
    )
    primary_other = models.CharField(
        "Other",
        max_length=35
    )
    secondary = models.CharField(
        "Secondary interest",
        max_length=35,
        choices=SECONDARY_INTEREST
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
    

class K12EducatorInformation(BasePersonalInformation,BaseEmployerInformation):
    
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
        choices=PRIMARY_INTEREST
    )
    primary_other = models.CharField(
        "Other",
        max_length=35
    )
    secondary = models.CharField(
        "Secondary interest",
        max_length=35,
        choices=SECONDARY_INTEREST
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
