# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import models, connection
from django.contrib.auth.models import User        

YES_NO = (
    ('yes','Yes'),
    ('no','No'),
)

PROFESSION = (
    ('undergrad','Undergraduate'),
    ('graduate','Graduate'),
    ('professional','Professional'),
    ('professor','Professor'),
    ('k12educator','K12 Educator'),
)

SALUTATION = (
    ('mr','Mr'),
    ('ms','Ms'),
    ('mrs','Mrs'),
    ('dr','Dr'),
)

STATES = (
    ('AL','Alabama'),
    ('AK','Alaska'),
    ('AZ','Arizona'),
    ('AR','Arkansas'),
    ('CA','California'),
    ('CO','Colorado'),
    ('CT','Connecticut'),
    ('DE','Delaware'),
    ('FL','Florida'),
    ('GA','Georgia'),
    ('HI','Hawaii'),
    ('ID','Idaho'),
    ('IL','Illinois'),
    ('IN','Indiana'),
    ('IA','Iowa'),
    ('KS','Kansas'),
    ('KY','Kentucky'),
    ('LA','Louisiana'),
    ('ME','Maine'),
    ('MD','Maryland'),
    ('MA','Massachusetts'),
    ('MI','Michigan'),
    ('MN','Minnesota'),
    ('MS','Mississippi'),
    ('MO','Missouri'),
    ('MT','Montana'),
    ('NE','Nebraska'),
    ('NV','Nevada'),
    ('NH','New Hampsire'),
    ('NJ','New Jersey'),
    ('NM','New Mexico'),
    ('NY','New York'),
    ('NC','North Carolina'),
    ('ND','North Dakota'),
    ('OH','Ohio'),
    ('OK','Oklahoma'),
    ('OR','Oregon'),
    ('PA','Pennsylvania'),
    ('RI','Rhode Island'),
    ('SC','South Carolina'),
    ('SD','South Dakota'),
    ('TN','Tennessee'),
    ('TX','Texas'),
    ('UT','Utah'),
    ('VT','Vermont'),
    ('WA','Washington'),
    ('WV','West Virginia'),
    ('WI','Wisconsin'),
    ('WY','Wyoming')
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

GENDER = (
    ('male','Male'),
    ('female','Female')
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


class PersonalInformation(models.Model):
    """
    Personal information when registering
    """
    
    rocket_contest = models.BooleanField(
        "Tribal or AISES Competition"
    )
    citizenship = models.CharField(
        "US Citizenship",
        max_length=3,
        choices=YES_NO
    )
    profession = models.CharField(
        "Profession",
        max_length=11,
        choices=PROFESSION
    )
    salutation = models.CharField(
        "Salutation",
        max_length=3,
        choices=SALUTATION
    )
    first = models.CharField(
        "First Name",
        max_length=20
    )
    middle = models.CharField(
        "Middle Name",
        max_length=15,
        blank=True
    )
    last = models.CharField(
        "Last Name",
        max_length=20
    )
    maiden_name = models.CharField(
        "Maiden Name",
        max_length=20,
        blank=True
    )
    #Do we need additional name? -zw
    additional_name = models.CharField(
        "Additional name",
        max_length=20,
        blank=True
    )
    title_department = models.CharField(
        "Title or Department",
        max_length=40,
        blank=True
    )
    #Consider renaming "web page" -zw
    web_page = models.CharField(
        "Web page",
        max_length=50,
        blank=True
    )

class AddressInformation(models.Model):
    """
    Address information when registering
    """
    
    street = models.CharField(
        "Street",
        max_length=35
    )
    city = models.CharField(
        "City",
        max_length=25
    )
    state = models.CharField(
        "State",
        max_length=2,
        choices=STATES
    )
    zip_code = models.CharField(
        "Zip Code",
        max_length=10
    )
    phone = models.CharField(
        "Phone number",
        max_length=16
    )
    primary_interest = models.CharField(
        "Primary Interest",
        max_length=50,
        choices=PRIMARY_INTEREST
    )
    primary_interest_other = models.CharField(
        "Other primary interest",
        max_length=50
    )
    secondary_interest = models.CharField(
        "Secondary Interest",
        max_length=50,
        choices=SECONDARY_INTEREST
    )
    birthdate = models.DateField(
        "Birthdate",
        auto_now=False
    )
    gender = models.CharField(
        "Gender",
        max_length=8,
        choices=GENDER
    )
    disability = models.BooleanField(
        "Disability"
    )
    race = models.CharField(
        "Race",
        max_length=40,
        choices=RACE
    )
    tribe = models.CharField(
        "Tribe",
        max_length=55
    )
    first_sibling = models.CharField(
        "First sibling to graduate",
        max_length=3,
        choices=YES_NO
    )
    subsidized_lunch = models.CharField(
        "Subsidized school lunch",
        max_length=3,
        choices=YES_NO
    )
    us_veteran = models.CharField(
        "US Military Veteran",
        max_length=3,
        choices=YES_NO
    )