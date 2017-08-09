django-djspace
==============

Wisconsin Space Grant Consortium grant programs application infrastructure.

# New Data Model

1. create data model class in application/models.py

2. update the applications GM2MField in the UserProfile() data model class with the name of the new class e.g. 'application.NewDataModel',

3. create the form class in application/forms.py

4. execute 'python manage.py migrate --run-syncdb' to create the new table(s). if the table is created but the command barfed, check the django_content_type table to insure that the ContentType object was created. if not, do it manually.

5. update templates/dashboard/applications.inc.html to add the URL to the application form

6. create admin class in application/admin.py

7. email template for after submission and print view on admin dashboard

8. update application/views.py if need be

9. update templates/application/form.html if need be

_Faculty_

Aerospace Outreach
Create Rocket Launch Team (NOI)
Higher Education Initiatives
NASA Competition
Research Infrastructure
Special Initiatives

_Professional_

Aerospace Outreach
Industry Internship
Higher Education Initiatives
NASA Competition
Research Infrastructure
Special Initiatives

_UnderGraduate_

Dr. Laurel Salton Clark Memorial Research Fellowship
Collegiate Rocket Launch Competition
First Nations Rocket Launch Competition
Midwest High-Powered Rocket Launch Competition
High Altitude Balloon Payload
High Altitude Balloon Launch
Professional Program Student Participation
STEM Bridge Scholarship
Undergraduate Scholarship
Undergraduate Research Fellowship
WSGC Graduate & Professional Research Fellowship

_Graduate_

Dr. Laurel Salton Clark Memorial Research Fellowship
WSGC Graduate & Professional Research Fellowship
