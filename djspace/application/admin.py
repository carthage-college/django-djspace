# -*- coding: utf-8 -*-
from django import forms
from django.conf import settings
from django.contrib import admin
from django.contrib import messages
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.utils.text import Truncator
from django.utils.html import strip_tags
from django.utils.encoding import smart_bytes
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy
from django.contrib.admin.helpers import ActionForm
from django.template import loader

from djspace.application.models import *
from djspace.core.utils import admin_display_file, get_start_date
from djspace.core.admin import GenericAdmin, PROFILE_LIST_DISPLAY
from djspace.core.models import UserFiles
from djspace.registration.admin import PROFILE_HEADERS, get_profile_fields
from djtools.fields import TODAY

from openpyxl import load_workbook
from openpyxl.writer.excel import save_virtual_workbook
from io import BytesIO

import tarfile
import glob
import csv
import io
import os

FUNDED_FILES = (
    ('','---Select---'),
    ('biography','Biography'),
    ('critical_design_report','Critical Design Report'),
    ('cv','CV'),
    ('education_outreach','Education Outreach'),
    ('final_design_report','Final Design Report'),
    ('final_report','Final Report'),
    ('flight_demo','Flight Demo'),
    ('flight_readiness_report','Flight Readiness Report'),
    ('interim_progress_report','Interim Progress Report'),
    ('interim_report','Interim Report'),
    ('invoice','Invoice'),
    ('lodging_list','Lodging List'),
    ('media_release','Media Release'),
    ('mugshot','Mugshot'),
    ('oral_presentation','Oral Presentation'),
    ('payment_information','Payment Information'),
    ('post_flight_performance_report','Post Flight Performance Report'),
    ('preliminary_design_report','Preliminary Design Report'),
    ('program_match','Program Match'),
    ('proposal','Proposal'),
    ('irs_w9','W9'),
    #('',''),

)


def required_files(modeladmin, request, queryset):
    """
    export required program files for all applicants to a tarball
    """
    if not queryset:
        messages.add_message(
            request, messages.ERROR,
            '''
                Currently, there are no applications for this program.
            ''',
            extra_tags='danger'
        )
        return HttpResponseRedirect(
            reverse_lazy(
                "admin:application_{}_changelist".format(object_name.lower())
            )
        )
    else:
        object_name = modeladmin.model._meta.object_name
        response = HttpResponse(content_type='application/x-gzip')
        response['Content-Disposition'] = 'attachment; filename={}.tar.gz'.format(
            object_name
        )
        tar_ball = tarfile.open(fileobj=response, mode='w:gz')
        for obj in queryset:
            for field in obj.required_files():
                if field != "media_release":
                    phile = getattr(obj, field)
                else:
                    phile = obj.user.user_files.media_release
                if phile:
                    path = phile.path
                    path_list = path.split('/')
                    name = path_list[-1]
                    tar_ball.add(path, arcname=name)
        tar_ball.close()
        return response


def export_required_files(modeladmin, request, queryset):
    """
    Export required files
    """

    return required_files(modeladmin, request, queryset)

export_required_files.short_description = "Export Required Files"


def longitudinal_tracking(modeladmin, request):
    """
    Export application data to OpenXML file
    """
    users = User.objects.all().order_by('last_name')
    program = None
    exports = []
    for user in users:
        try:
            apps = user.profile.applications.all()
        except:
            apps = None
        if apps:
            for a in apps:
                if a._meta.object_name == modeladmin.model._meta.object_name \
                and a.status:
                    exports.append({'user':user,'app':a})
                    #program = a.get_application_type()
                    program = a.get_slug()

    wb = load_workbook(
        '{}/application/longitudinal_tracking.xlsx'.format(settings.ROOT_DIR)
    )
    ws = wb.active
    # this could all be accomplished by a list of lists but building a list
    # for each row would be ugly. this seems more pythonic, and we can reuse
    # for CSV export if need be.
    t = loader.get_template('application/export.longitudinal.html')
    c = { 'exports': exports, 'program':program, 'year':TODAY.year }
    data = smart_bytes(
        t.render(c), encoding='utf-8', strings_only=False, errors='strict'
    )

    # reader requires an object which supports the iterator protocol and
    # returns a string each time its next() method is called. StringIO
    # provides an in-memory, line by line stream of the template data.
    #reader = csv.reader(io.StringIO(data), delimiter="|")
    reader = csv.reader(BytesIO(data), delimiter="|")
    for row in reader:
        ws.append(row)

    # in memory response instead of save to file system
    response = HttpResponse(
        save_virtual_workbook(wb), content_type='application/ms-excel'
    )

    response['Content-Disposition'] = 'attachment;filename={}.xlsx'.format(
        program
    )

    return response


def export_longitudinal_tracking(modeladmin, request, extra_context=None):
    """
    Export application data to CSV for NASA reporting requirements
    """

    return longitudinal_tracking(modeladmin, request)

export_longitudinal_tracking.short_description = "Export Longitudinal Tracking"


def export_applications(modeladmin, request, queryset, reg_type=None):
    """
    Export application data to CSV
    """

    file_fields = [
        "cv", "proposal", "letter_interest",
        "budget", "undergraduate_transcripts", "graduate_transcripts",
        "recommendation", "recommendation_1", "recommendation_2",
        "high_school_transcripts", "wsgc_advisor_recommendation",
        "statement"
    ]
    exclude = [
        "user", "userprofile", "user_id", "updated_by_id", "id",
        "aerospaceoutreach", "clarkgraduatefellowship",
        "first_nations_rocket_competition", "collegiate_rocket_competition",
        "midwest_high_powered_rocket_competition", "graduatefellowship",
        "highaltitudeballoonpayload","highaltitudeballoonlaunch",
        "highereducationinitiatives", "industryinternship","nasacompetition",
        "researchinfrastructure", "specialinitiatives",
        "undergraduateresearch", "undergraduatescholarship"
    ]

    field_names = [f.name for f in modeladmin.model._meta.get_fields()]
    headers = PROFILE_HEADERS + field_names
    # remove unwanted headers
    for e in exclude:
        if e in headers:
            headers.remove(e)

    bi = BytesIO()
    csv.register_dialect('pipes', delimiter='|')
    writer = csv.writer(bi, dialect='pipes')
    writer.writerow(headers)

    for reg in queryset:
        fields = get_profile_fields(reg)
        field_names = [f.name for f in reg._meta.get_fields()]
        for field in field_names:
            if field and field not in exclude:
                value = getattr(reg, field, None)
                if value != '':
                    if field == 'synopsis':
                        value = unicode(
                            strip_tags(value)
                        ).encode('utf-8', 'ignore').strip()
                    elif field in file_fields:
                        earl = 'https://{}{}{}'.format(
                            settings.SERVER_URL, settings.MEDIA_URL, value
                        )
                        value = '=HYPERLINK("{}","{}")'.format(earl, field)
                    else:
                        value = unicode(value).encode('utf-8', 'ignore')
                fields.append(value)
        writer.writerow(fields)

    wb = load_workbook(
        '{}/application/applications.xlsx'.format(settings.ROOT_DIR)
    )
    ws = wb.active

    reader = csv.reader(BytesIO(bi.getvalue()), dialect='pipes')

    for row in reader:
        ws.append(row)

    # in memory response instead of save to file system
    response = HttpResponse(
        save_virtual_workbook(wb), content_type='application/ms-excel'
    )

    response['Content-Disposition'] = 'attachment;filename={}.xlsx'.format(
        reg.get_slug()
    )

    return response


def export_all_applications(modeladmin, request, queryset):
    """
    Export application data to CSV for all registration types
    """

    return export_applications(modeladmin, request, queryset)

export_all_applications.short_description = "Export All Applications"


def _build_tarball(queryset, object_name, field, userfiles=False):

    response = HttpResponse(content_type='application/x-gzip')
    response['Content-Disposition'] = 'attachment; filename={}_{}.tar.gz'.format(
        object_name, field
    )

    tar_ball = tarfile.open(fileobj=response, mode='w:gz')
    for obj in queryset:
        if userfiles:
            # some users might not have a user_files relationship
            try:
                obj = obj.user.user_files
            except:
                continue
        phile = getattr(obj, field, None)
        if phile:
            path = phile.path
            path_list = path.split('/')
            name = path_list[-1]
            tar_ball.add(path, arcname=name)
    tar_ball.close()

    return response


def export_funded_files(modeladmin, request, queryset):
    """
    Generate a tarball of files for funded programs
    """
    phile = request.POST['phile']
    if not phile:
        messages.add_message(
            request, messages.ERROR,
            'You must choose a file name.',
            extra_tags='danger'
        )
    else:
        object_name = modeladmin.model._meta.object_name
        if phile in [f.name for f in modeladmin.model._meta.get_fields()]:
            response = _build_tarball(queryset, object_name, phile)
            return response
        elif phile in [f.name for f in UserFiles._meta.get_fields()]:
            response = _build_tarball(
                queryset, object_name, phile, userfiles=True
            )
            return response
        else:
            messages.add_message(
                request, messages.ERROR,
                'The file you requested is not in the current program.',
                extra_tags='danger'
            )

export_funded_files.short_description = "Export Funded Files"


class TarballActionForm(ActionForm):
    phile = forms.CharField(
        label="File name",
        required=False,
        widget=forms.Select(choices=FUNDED_FILES)
    )


class HighAltitudeBalloonPayloadAdmin(GenericAdmin):

    model = HighAltitudeBalloonLaunch

    list_display  = PROFILE_LIST_DISPLAY + [
        'cv_file', 'commit_short', 'letter_interest_file',
        'date_created','date_updated','past_funding','past_funding_year',
        'funded_code','status'
    ]
    list_editable = ['funded_code','status']
    action_form = TarballActionForm
    actions = [
        export_longitudinal_tracking, export_all_applications,
        export_required_files, export_funded_files,
        'email_applicants'
    ]

    def cv_file(self, instance):
        return admin_display_file(instance,"cv")
    cv_file.allow_tags = True
    cv_file.short_description = "CV"

    def commit_short(self, instance):
        return instance.commit
    commit_short.short_description = "Commitement"

    def letter_interest_file(self, instance):
        return admin_display_file(instance,"letter_interest")
    letter_interest_file.allow_tags = True
    letter_interest_file.short_description = "Interest"


class HighAltitudeBalloonLaunchAdmin(HighAltitudeBalloonPayloadAdmin):

    model = HighAltitudeBalloonLaunch

    list_display  = PROFILE_LIST_DISPLAY + [
        'cv_file', 'letter_interest_file',
        'date_created','date_updated','past_funding','past_funding_year',
        'funded_code','status'
    ]


class ClarkGraduateFellowshipAdmin(GenericAdmin):

    model = ClarkGraduateFellowship

    list_display  = PROFILE_LIST_DISPLAY + [
        'signed_certification','proposal_file','cv_file', 'budget_file',
        'undergraduate_transcripts_file','graduate_transcripts_file',
        'recommendation_1_file','recommendation_2_file',
        'project_title','begin_date','end_date',
        'anticipating_funding','funds_requested','funds_authorized',
        'synopsis_trunk','date_created','date_updated',
        'past_funding','past_funding_year','funded_code','status'
    ]
    list_editable = ['funds_authorized','funded_code','status']
    list_display_links = ['project_title']
    action_form = TarballActionForm
    actions = [
        export_longitudinal_tracking, export_all_applications,
        export_required_files, export_funded_files,
        'email_applicants'
    ]

    def synopsis_trunk(self, instance):
        return Truncator(instance.synopsis).words(
            25, html=True, truncate=" ..."
        )
    synopsis_trunk.allow_tags = True
    synopsis_trunk.short_description = "Synopsis truncated"

    def proposal_file(self, instance):
        return admin_display_file(instance,"proposal")
    proposal_file.allow_tags = True
    proposal_file.short_description = 'Proposal'

    def cv_file(self, instance):
        return admin_display_file(instance,"cv")
    cv_file.allow_tags = True
    cv_file.short_description = "CV"

    def budget_file(self, instance):
        return admin_display_file(instance,"budget")
    budget_file.allow_tags = True
    budget_file.short_description = "Budget"

    def undergraduate_transcripts_file(self, instance):
        return admin_display_file(instance,"undergraduate_transcripts")
    undergraduate_transcripts_file.allow_tags = True
    undergraduate_transcripts_file.short_description = "UG Trans"

    def graduate_transcripts_file(self, instance):
        return admin_display_file(instance,"graduate_transcripts")
    graduate_transcripts_file.allow_tags = True
    graduate_transcripts_file.short_description = "GR Trans"

    def recommendation_1_file(self, instance):
        return admin_display_file(instance,"recommendation_1")
    recommendation_1_file.allow_tags = True
    recommendation_1_file.short_description = "Recom 1"

    def recommendation_2_file(self, instance):
        return admin_display_file(instance,"recommendation_2")
    recommendation_2_file.allow_tags = True
    recommendation_2_file.short_description = "Recom 2"


class GraduateFellowshipAdmin(ClarkGraduateFellowshipAdmin):

    model = GraduateFellowship


class UndergraduateAdmin(GenericAdmin):
    """
    base admin class for the various undergrad applications
    """

    action_form = TarballActionForm
    actions = [
        export_longitudinal_tracking, export_all_applications,
        export_required_files, export_funded_files,
        'email_applicants'
    ]

    def high_school_transcripts_file(self, instance):
        return admin_display_file(instance,"high_school_transcripts")
    high_school_transcripts_file.allow_tags = True
    high_school_transcripts_file.short_description = "HS Trans"

    def undergraduate_transcripts_file(self, instance):
        return admin_display_file(instance,"undergraduate_transcripts")
    undergraduate_transcripts_file.allow_tags = True
    undergraduate_transcripts_file.short_description = "UG Trans"

    def wsgc_advisor_recommendation_file(self, instance):
        return admin_display_file(instance,"wsgc_advisor_recommendation")
    wsgc_advisor_recommendation_file.allow_tags = True
    wsgc_advisor_recommendation_file.short_description = "WSGC Advisor Recom"

    def recommendation_file(self, instance):
        return admin_display_file(instance,"recommendation")
    recommendation_file.allow_tags = True
    recommendation_file.short_description = "Recommendation"


class UndergraduateResearchAdmin(UndergraduateAdmin):

    model = UndergraduateResearch

    list_display  = PROFILE_LIST_DISPLAY + [
        'signed_certification','proposal_file',
        'high_school_transcripts_file','undergraduate_transcripts_file',
        'wsgc_advisor_recommendation_file','recommendation_file',
        'project_title', 'begin_date', 'end_date',
        'funds_requested','funds_authorized',
        'other_funding', 'other_funding_explain',
        'synopsis_trunk',
        'other_funding', 'other_funding_explain',
        'date_created','date_updated',
        'past_funding','past_funding_year','funded_code','status'
    ]
    list_editable = ['funds_authorized','funded_code','status']
    list_display_links = ['project_title']

    def synopsis_trunk(self, instance):
        return Truncator(instance.synopsis).words(
            25, html=True, truncate=" ..."
        )
    synopsis_trunk.allow_tags = True
    synopsis_trunk.short_description = "Synopsis truncated"

    def proposal_file(self, instance):
        return admin_display_file(instance,"proposal")
    proposal_file.allow_tags = True
    proposal_file.short_description = 'Proposal'


class UndergraduateScholarshipAdmin(UndergraduateAdmin):

    model = UndergraduateScholarship

    list_display  = PROFILE_LIST_DISPLAY + [
        'signed_certification','statement_file',
        'high_school_transcripts_file','undergraduate_transcripts_file',
        'wsgc_advisor_recommendation_file','recommendation_file',
        'academic_institution','wsgc_affiliate',
        'other_funding', 'other_funding_explain',
        'date_created','date_updated',
        'past_funding','past_funding_year','funded_code','status'
    ]
    list_editable = ['funded_code','status']

    def statement_file(self, instance):
        return admin_display_file(instance,"statement")
    statement_file.allow_tags = True
    statement_file.short_description = 'Statement'


class StemBridgeScholarshipAdmin(UndergraduateScholarshipAdmin):

    model = StemBridgeScholarship


class RocketLaunchTeamAdmin(GenericAdmin):

    model = RocketLaunchTeam

    action_form = TarballActionForm
    actions = [
        export_longitudinal_tracking, export_all_applications,
        export_required_files, export_funded_files,
        'email_applicants'
    ]

    list_display  = PROFILE_LIST_DISPLAY + [
        'budget_file',
        'interim_progress_report_file','preliminary_design_report_file',
        'final_design_report_file','flight_demo_file',
        'final_motor_selection_trunk','lodging_list_file',
        'critical_design_report_file','post_flight_performance_report_file',
        'education_outreach_file','flight_readiness_report_file',
        'proceeding_paper_file',
        'name','academic_institution_name','competition','co_advisor','leader',
        'industry_mentor_name','industry_mentor_email',
        'date_created','date_updated',
        'past_funding','past_funding_year','funded_code','status'
    ]
    list_display_links = ['name']
    list_editable = ['funded_code','status']
    raw_id_fields = ('user','co_advisor','leader','members',)

    def budget_file(self, instance):
        return admin_display_file(instance,'budget')
    budget_file.allow_tags = True
    budget_file.short_description = "Budget"

    def interim_progress_report_file(self, instance):
        return admin_display_file(instance,'interim_progress_report')
    interim_progress_report_file.allow_tags = True
    interim_progress_report_file.short_description = "Interim Rpt"

    def preliminary_design_report_file(self, instance):
        return admin_display_file(instance,'preliminary_design_report')
    preliminary_design_report_file.allow_tags = True
    preliminary_design_report_file.short_description = "Prelim Design Rpt"

    def final_design_report_file(self, instance):
        return admin_display_file(instance,'final_design_report')
    final_design_report_file.allow_tags = True
    final_design_report_file.short_description = "Final Design Rpt"

    def flight_demo_file(self, instance):
        icon = '<i class="fa fa-times-circle red" aria-hidden="true"></i>'
        if instance.flight_demo:
            icon = '''
              <i class="fa fa-check green" aria-hidden="true" title="{}"></i>
            '''.format(instance.flight_demo)
        return icon
    flight_demo_file.allow_tags = True
    flight_demo_file.short_description = "Flight Demo URL"

    def final_motor_selection_trunk(self, instance):
        return Truncator(instance.final_motor_selection).words(
            25, html=True, truncate=" ..."
        )
    final_motor_selection_trunk.allow_tags = True
    final_motor_selection_trunk.short_description = "Final Motor"

    def lodging_list_file(self, instance):
        return admin_display_file(instance,'lodging_list')
    lodging_list_file.allow_tags = True
    lodging_list_file.short_description = "Lodging"

    def critical_design_report_file(self, instance):
        return admin_display_file(instance,'critical_design_report')
    critical_design_report_file.allow_tags = True
    critical_design_report_file.short_description = "Critical design"

    def oral_presentation_file(self, instance):
        return admin_display_file(instance,'oral_presentation')
    oral_presentation_file.allow_tags = True
    oral_presentation_file.short_description = "Oral Pres."

    def post_flight_performance_report_file(self, instance):
        return admin_display_file(instance,'post_flight_performance_report')
    post_flight_performance_report_file.allow_tags = True
    post_flight_performance_report_file.short_description = "Post flight"

    def education_outreach_file(self, instance):
        return admin_display_file(instance,'education_outreach')
    education_outreach_file.allow_tags = True
    education_outreach_file.short_description = "Edu. Outreach"

    def flight_readiness_report_file(self, instance):
        return admin_display_file(instance,'flight_readiness_report')
    flight_readiness_report_file.allow_tags = True
    flight_readiness_report_file.short_description = "Flight Ready"

    def proceeding_paper_file(self, instance):
        icon = '<i class="fa fa-times-circle red" aria-hidden="true"></i>'
        if instance.proceeding_paper:
            icon = '''
              <i class="fa fa-check green" aria-hidden="true" title="{}"></i>
            '''.format(instance.proceeding_paper)
        return icon
    proceeding_paper_file.allow_tags = True
    proceeding_paper_file.short_description = "Proceeding Paper Date"


class CollegiateRocketCompetitionAdmin(GenericAdmin):

    model = CollegiateRocketCompetition

    list_display  = PROFILE_LIST_DISPLAY + [
        'cv_file','team','date_created','date_updated',
        'past_funding','past_funding_year','funded_code','status'
    ]
    list_display_links = ['team']
    list_editable = ['funded_code','status']

    action_form = TarballActionForm
    actions = [
        export_longitudinal_tracking, export_all_applications,
        export_required_files, export_funded_files,
        'email_applicants'
    ]

    def cv_file(self, instance):
        return admin_display_file(instance,"cv")
    cv_file.allow_tags = True
    cv_file.short_description = "CV"


class MidwestHighPoweredRocketCompetitionAdmin(GenericAdmin):

    model = MidwestHighPoweredRocketCompetition

    list_display  = PROFILE_LIST_DISPLAY + [
        'team','date_created','date_updated','cv_file',
        'past_funding','past_funding_year','funded_code','status'
    ]
    list_display_links = ['team']
    list_editable = ['funded_code','status']

    action_form = TarballActionForm
    actions = [
        export_longitudinal_tracking, export_all_applications,
        export_required_files, export_funded_files,
        'email_applicants'
    ]

    def cv_file(self, instance):
        return admin_display_file(instance,"cv")
    cv_file.allow_tags = True
    cv_file.short_description = "CV"


class FirstNationsRocketCompetitionAdmin(GenericAdmin):

    model = FirstNationsRocketCompetition

    list_display  = PROFILE_LIST_DISPLAY + [
        'team','date_created','date_updated',
        'past_funding','past_funding_year','funded_code','status'
    ]
    list_display_links = ['team']
    list_editable = ['funded_code','status']

    action_form = TarballActionForm
    actions = [
        export_longitudinal_tracking, export_all_applications,
        export_required_files, export_funded_files,
        'email_applicants'
    ]


class HigherEducationInitiativesAdmin(GenericAdmin):

    model = HigherEducationInitiatives

    list_display  = PROFILE_LIST_DISPLAY + [
        'invoice_file','program_match_file','payment_information_file',
        'project_title','begin_date','end_date','award_type',
        'funds_requested','funds_authorized',
        'proposed_match','authorized_match','source_match','location',
        'synopsis_trunk','proposal_file',
        'finance_officer_name','finance_officer_address',
        'finance_officer_email','finance_officer_phone',
        'grant_officer_name','grant_officer_address',
        'grant_officer_email','grant_officer_phone',
        'date_created','date_updated',
        'past_funding','past_funding_year','funded_code','status'
    ]
    list_editable = [
        'funds_authorized','authorized_match','funded_code','status'
    ]
    list_display_links = ['project_title']

    action_form = TarballActionForm
    actions = [
        export_longitudinal_tracking, export_all_applications,
        export_required_files, export_funded_files,
        'email_applicants'
    ]

    def synopsis_trunk(self, instance):
        return Truncator(instance.synopsis).words(
            25, html=True, truncate=" ..."
        )
    synopsis_trunk.allow_tags = True
    synopsis_trunk.short_description = "Synopsis truncated"

    def proposal_file(self, instance):
        return admin_display_file(instance,"proposal")
    proposal_file.allow_tags = True
    proposal_file.short_description = 'Proposal'

    def invoice_file(self, instance):
        return admin_display_file(instance,"invoice")
    invoice_file.allow_tags = True
    invoice_file.short_description = "Invoice"

    def program_match_file(self, instance):
        return admin_display_file(instance,"program_match")
    program_match_file.allow_tags = True
    program_match_file.short_description = "Program match"

    def payment_information_file(self, instance):
        return admin_display_file(instance,"payment_information")
    payment_information_file.allow_tags = True
    payment_information_file.short_description = "Payment information"


class ResearchInfrastructureAdmin(HigherEducationInitiativesAdmin):

    model = ResearchInfrastructure


class AerospaceOutreachAdmin(HigherEducationInitiativesAdmin):

    model = AerospaceOutreach

    list_display  = PROFILE_LIST_DISPLAY + [
        'invoice_file','program_match_file','payment_information_file',
        'project_title','begin_date','end_date','project_category',
        'proposal_file','funds_requested','funds_authorized',
        'other_funding','other_funding_explain',
        'proposed_match','authorized_match','source_match','location',
        'synopsis_trunk',
        'finance_officer_name','finance_officer_address',
        'finance_officer_email','finance_officer_phone',
        'grant_officer_name','grant_officer_address',
        'grant_officer_email','grant_officer_phone',
        'date_created','date_updated',
        'past_funding','past_funding_year','funded_code','status'
    ]


class NasaCompetitionAdmin(GenericAdmin):

    model = NasaCompetition

    list_display  = PROFILE_LIST_DISPLAY + [
        'invoice_file','program_match_file','payment_information_file',
        'statement_file','budget_file',
        'competition_type','competition_type_other',
        'facility_name','facility_name_other',
        'program_acceptance','award_type',
        'begin_date','end_date','funds_requested','funds_authorized',
        'proposed_match','authorized_match','source_match',
        'finance_officer_name','finance_officer_address',
        'finance_officer_email','finance_officer_phone',
        'grant_officer_name','grant_officer_address',
        'grant_officer_email','grant_officer_phone',
        'date_created','date_updated',
        'past_funding','past_funding_year','funded_code','status'
    ]
    list_display_links = ['date_created']
    list_editable = [
        'funds_authorized','authorized_match','funded_code','status'
    ]
    #date_created.short_description = 'Created (edit)'

    action_form = TarballActionForm
    actions = [
        export_longitudinal_tracking, export_all_applications,
        export_required_files, export_funded_files,
        'email_applicants'
    ]

    def budget_file(self, instance):
        return admin_display_file(instance,"budget")
    budget_file.allow_tags = True
    budget_file.short_description = "Budget"

    def statement_file(self, instance):
        return admin_display_file(instance,"statement")
    statement_file.allow_tags = True
    statement_file.short_description = 'Statement'

    def invoice_file(self, instance):
        return admin_display_file(instance,"invoice")
    invoice_file.allow_tags = True
    invoice_file.short_description = "Invoice"

    def program_match_file(self, instance):
        return admin_display_file(instance,"program_match")
    program_match_file.allow_tags = True
    program_match_file.short_description = "Program match"

    def payment_information_file(self, instance):
        return admin_display_file(instance,"payment_information")
    payment_information_file.allow_tags = True
    payment_information_file.short_description = "Payment information"


class SpecialInitiativesAdmin(AerospaceOutreachAdmin):

    model = SpecialInitiatives


class WorkPlanTaskInline(admin.TabularInline):
    model = WorkPlanTask
    fields = ('title', 'description', 'hours_percent','expected_outcome')


class IndustryInternshipAdmin(GenericAdmin):

    list_display  = PROFILE_LIST_DISPLAY + [
        'budget_file','invoice_file','program_match_file',
        'payment_information_file','award_type',
        'funds_requested','funds_authorized',
        'proposed_match','authorized_match','source_match',
        'date_created','date_updated',
        'past_funding','past_funding_year','funded_code','status'
    ]

    model = IndustryInternship
    list_display_links = ['first_name']
    list_editable = [
        'funds_authorized','authorized_match','funded_code','status'
    ]

    action_form = TarballActionForm
    actions = [
        export_longitudinal_tracking, export_all_applications,
        export_required_files, export_funded_files,
        'email_applicants'
    ]

    inlines = [WorkPlanTaskInline,]

    def budget_file(self, instance):
        return admin_display_file(instance,"budget")
    budget_file.allow_tags = True
    budget_file.short_description = "Budget"

    def invoice_file(self, instance):
        return admin_display_file(instance,"invoice")
    invoice_file.allow_tags = True
    invoice_file.short_description = "Invoice"

    def program_match_file(self, instance):
        return admin_display_file(instance,"program_match")
    program_match_file.allow_tags = True
    program_match_file.short_description = "Program match"

    def payment_information_file(self, instance):
        return admin_display_file(instance,"payment_information")
    payment_information_file.allow_tags = True
    payment_information_file.short_description = "Payment information"


class ProfessionalProgramStudentAdmin(GenericAdmin):

    model = ProfessionalProgramStudent

    list_display  = PROFILE_LIST_DISPLAY + [
        'program_link','program_application_link','mentor',
        'date_created','date_updated',
        'past_funding','past_funding_year','funded_code','status'
    ]
    list_editable = ['funded_code','status']

    actions = [
        export_longitudinal_tracking, export_all_applications,
        'email_applicants'
    ]

    def program_application_link(self, instance):
        return instance.program_application_link()
    program_application_link.allow_tags = True
    program_application_link.short_description = "Program Application"

    def program_link(self, obj):
        link = '<a href="{}">{}</a>'.format(
            reverse(
                "admin:application_professionalprogramstudent_change",
                args=(obj.id,)
            ),
            obj.program
        )
        return link
    program_link.allow_tags = True
    program_link.short_description = 'Program Name (view/edit)'


'''
class WorkPlanTaskAdmin(admin.ModelAdmin):

    model = WorkPlanTask
    list_display = ['title','industry_internship',]
    raw_id_fields = ("industry_internship",)
'''

admin.site.register(
    HigherEducationInitiatives, HigherEducationInitiativesAdmin
)
admin.site.register(
    ResearchInfrastructure, ResearchInfrastructureAdmin
)
admin.site.register(
    AerospaceOutreach, AerospaceOutreachAdmin
)
admin.site.register(
    SpecialInitiatives, SpecialInitiativesAdmin
)
admin.site.register(
    RocketLaunchTeam, RocketLaunchTeamAdmin
)
admin.site.register(
    FirstNationsRocketCompetition, FirstNationsRocketCompetitionAdmin
)
admin.site.register(
    CollegiateRocketCompetition, CollegiateRocketCompetitionAdmin
)
admin.site.register(
    MidwestHighPoweredRocketCompetition, MidwestHighPoweredRocketCompetitionAdmin
)
admin.site.register(
    HighAltitudeBalloonLaunch, HighAltitudeBalloonLaunchAdmin
)
admin.site.register(
    HighAltitudeBalloonPayload, HighAltitudeBalloonPayloadAdmin
)
admin.site.register(
    ClarkGraduateFellowship, ClarkGraduateFellowshipAdmin
)
admin.site.register(
    GraduateFellowship, GraduateFellowshipAdmin
)
admin.site.register(
    NasaCompetition, NasaCompetitionAdmin
)
admin.site.register(
    StemBridgeScholarship, StemBridgeScholarshipAdmin
)
admin.site.register(
    UndergraduateScholarship, UndergraduateScholarshipAdmin
)
admin.site.register(
    UndergraduateResearch, UndergraduateResearchAdmin
)
admin.site.register(
    IndustryInternship, IndustryInternshipAdmin
)
admin.site.register(
    ProfessionalProgramStudent, ProfessionalProgramStudentAdmin
)
'''
admin.site.register(
    WorkPlanTask, WorkPlanTaskAdmin
)
'''
