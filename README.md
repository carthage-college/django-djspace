django-djspace
==============

Wisconsin Space Grant Consortium grant programs application infrastructure.

# New Data Model

1. create data model class in application/models.py

2. update the applications GM2MField in the UserProfile() data model class with the name of the new class e.g. 'application.NewDataModel',

3. create the form class and the form upload class in application/forms.py

4. for production, execute 'python manage.py migrate --run-syncdb' to create the new table(s). for staging or development, use migrations. if the table is created but the command barfed, check the django_content_type table to insure that the ContentType object was created. if not, do it manually.

5. update templates/dashboard/applications.inc.html to add the URL to the application form

6. create admin class in application/admin.py

7. email template for after submission and print view on admin dashboard

8. update application/views.py if need be

9. update templates/application/form.html if need be

10. update the UPLOAD_FORMS dictionary with the name of the model in lowercase

# New Field added to a Model

add a new field:

1. add to applications/models.py

virtual_cdr
virtual_pdr
virtual_frr

2. in models.py, add timestamp method if it is a file field:

def virtual_cdr_timestamp(self):
    return self.get_file_timestamp('virtual_cdr')
etc

3. in models.py, add to list in required_files() method if it is required field:

def required_files(self):
    '''
    used when building a tarball of required files
    '''
    return [
        'budget'
    ]

4. add the fields to the database table manually or with migrations

5. in application/admin.py
    a. add to FUNDED_FILES tuple.
    b. add to list_display list in RocketLaunchTeamAdmin() model
    'interim_progress_report_file','virtual_cdr_file',
    'preliminary_design_report_file','virtual_pdr_file',
    etc
    c. create methods to display those fields from (b)

        def virtual_cdr_file(self, instance):
            return admin_display_file(instance,'virtual_cdr')
        virtual_cdr_file.allow_tags = True
        virtual_cdr_file.short_description = "VCDR"

      etc

6. add class names in the td tag to static/djspace/css/admin.css

  field-virtual_cdr_file
  field-virtual_pdr_file
  etc

7. in application/forms.py, add the field names to the upload form:

class RocketLaunchTeamUploadsForm(forms.ModelForm):

    class Meta:
        model = RocketLaunchTeam
        fields = (
            'award_acceptance','interim_progress_report',
            'preliminary_design_report','final_design_report',
            'flight_demo','lodging_list','other_file',
            'critical_design_report','oral_presentation',
            'post_flight_performance_report','education_outreach',
            'flight_readiness_report','proceeding_paper','proposal',
            'budget','verified_budget','close_out_finance_document',
            'invoice','charges_certification','institutional_w9',
            'virtual_cdr','virtual_pdr','virtual_frr'
        )


8. add fields to templates/application/email/rocket-launch-team.files.inc.html

    {% if data.virtual_cdr %}
    <li>
      <a href="{{media_url}}{{data.virtual_cdr}}">
        Virtual CDR
      </a>
      <ul>
        <li>Created: {{data.virtual_cdr_timestamp}}</li>
        <li>
          https://{{server_url}}{{media_url}}{{data.virtual_cdr}}
        </li>
      </ul>
    </li>
    {% else %}
      {% if data.status %}
    <li>Virtual CDR: Missing</li>
      {% endif %}
    {% endif %}

9. add upload fields to templates/dashboard/rocket_launch_team_files.inc.html


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
