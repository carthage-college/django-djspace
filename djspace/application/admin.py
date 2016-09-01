# -*- coding: utf-8 -*-
from django import forms
from django.conf import settings
from django.contrib import admin
from django.http import HttpResponse
from django.utils.text import Truncator
from django.utils.html import strip_tags
from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from django.shortcuts import render_to_response
from django.template import loader, Context, RequestContext

from djspace.application.models import *
from djspace.core.utils import get_start_date
from djspace.core.admin import GenericAdmin, PROFILE_LIST_DISPLAY
from djspace.registration.admin import PROFILE_HEADERS, get_profile_fields
from djtools.fields import TODAY

from openpyxl import load_workbook
from openpyxl.writer.excel import save_virtual_workbook

import csv
import io

def get_queryset(self, request, admin_class):
    """
    only show applications that were created after a certain date.
    they wanted to see only applications for the current grant cycle.
    so we hide old applications.
    """
    qs = super(admin_class, self).get_queryset(request)
    return qs.filter(date_created__gte=get_start_date())

def longitudinal_tracking(modeladmin, request):
    """
    Export application data to OpenXML file
    """
    users = User.objects.all().order_by("last_name")
    program = None
    exports = []
    for user in users:
        try:
            apps = user.profile.applications.all()
        except:
            apps = None
        if apps:
            for a in apps:
                if a._meta.object_name == modeladmin.model._meta.object_name and a.status:
                    exports.append({"user":user,"app":a})
                    #program = a.get_application_type()
                    program = a.get_slug()

    wb = load_workbook(
        '{}/application/logitudinal_tracking.xlsx'.format(settings.ROOT_DIR)
    )
    ws = wb.active
    # this could all be accomplished by a list of lists but building a list
    # for each row would be ugly. this seems more pythonic, and we can reuse
    # for CSV export if need be.
    t = loader.get_template('application/export.html')
    c = Context({ 'exports': exports, 'program':program, 'year':TODAY.year })
    data = t.render(c)
    # reader requires an object which supports the iterator protocol and
    # returns a string each time its next() method is called. StringIO
    # provides an in-memory, line by line stream of the template data.
    reader = csv.reader(io.StringIO(data), delimiter="|")
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


class HighAltitudeBalloonLaunchAdmin(GenericAdmin):

    model = HighAltitudeBalloonLaunch

    list_display  = PROFILE_LIST_DISPLAY + [
        'cv_link', 'letter_interest_link',
        'date_created','date_updated',
        'status'
    ]
    list_editable = ['status']
    actions = [export_longitudinal_tracking]

    def cv_link(self, instance):
        return '<a href="{}" target="_blank">CV</a>'.format(
            instance.cv.url
        )
    cv_link.allow_tags = True
    cv_link.short_description = "CV"

    def letter_interest_link(self, instance):
        return '<a href="{}" target="_blank">Letter</a>'.format(
            instance.letter_interest.url
        )
    letter_interest_link.allow_tags = True
    letter_interest_link.short_description = "Letter of interest"

    def get_queryset(self, request):
        qs = get_queryset(self, request, HighAltitudeBalloonLaunchAdmin)
        return qs


class HighAltitudeBalloonPayloadAdmin(HighAltitudeBalloonLaunchAdmin):

    model = HighAltitudeBalloonPayload

    def get_queryset(self, request):
        qs = get_queryset(self, request, HighAltitudeBalloonPayloadAdmin)
        return qs


class ClarkGraduateFellowshipAdmin(GenericAdmin):

    model = ClarkGraduateFellowship

    list_display  = PROFILE_LIST_DISPLAY + [
        'project_title', 'begin_date', 'end_date',
        'anticipating_funding', 'funds_requested', 'funds_authorized',
        'synopsis_trunk', 'signed_certification_link', 'proposal_link',
        'cv_link', 'budget_link', 'undergraduate_transcripts_link',
        'graduate_transcripts_link', 'recommendation_1_link',
        'recommendation_2_link', 'date_created','date_updated','status'
    ]
    list_editable = ['funds_authorized','status']
    list_display_links = ['project_title']
    actions = [export_longitudinal_tracking]

    def synopsis_trunk(self, instance):
        return Truncator(instance.synopsis).words(
            25, html=True, truncate=" ..."
        )
    synopsis_trunk.allow_tags = True
    synopsis_trunk.short_description = "Synopsis truncated"

    def signed_certification_link(self, instance):
        return '<a href="{}" target="_blank">Signed Certification</a>'.format(
            instance.signed_certification.url
        )
    signed_certification_link.allow_tags = True
    signed_certification_link.short_description = "Signed Certification"

    def proposal_link(self, instance):
        return '<a href="{}" target="_blank">Proposal</a>'.format(
            instance.proposal.url
        )
    proposal_link.allow_tags = True
    proposal_link.short_description = 'Proposal file'

    def cv_link(self, instance):
        return '<a href="{}" target="_blank">CV</a>'.format(
            instance.cv.url
        )
    cv_link.allow_tags = True
    cv_link.short_description = "CV"

    def budget_link(self, instance):
        return '<a href="{}" target="_blank">Budget</a>'.format(
            instance.budget.url
        )
    budget_link.allow_tags = True
    budget_link.short_description = "Budget"

    def undergraduate_transcripts_link(self, instance):
        return '<a href="{}" target="_blank">Undergraduate Transcripts</a>'.format(
            instance.undergraduate_transcripts.url
        )
    undergraduate_transcripts_link.allow_tags = True
    undergraduate_transcripts_link.short_description = "Undergraduate Transcripts"

    def graduate_transcripts_link(self, instance):
        return '<a href="{}" target="_blank">Graduate Transcripts</a>'.format(
            instance.graduate_transcripts.url
        )
    graduate_transcripts_link.allow_tags = True
    graduate_transcripts_link.short_description = "Graduate Transcripts"

    def recommendation_1_link(self, instance):
        try:
            code = '<a href="{}" target="_blank">Rec. 1</a>'.format(
                instance.recommendation_1.url
            )
        except:
            code = None
        return code

    recommendation_1_link.allow_tags = True
    recommendation_1_link.short_description = "Recommendation 1"

    def recommendation_2_link(self, instance):
        try:
            code = '<a href="{}" target="_blank">Rec. 2</a>'.format(
                instance.recommendation_2.url
            )
        except:
            code = None
        return code

    recommendation_2_link.allow_tags = True
    recommendation_2_link.short_description = "Recommendation 2"

    def get_queryset(self, request):
        qs = get_queryset(self, request, ClarkGraduateFellowshipAdmin)
        return qs


class GraduateFellowshipAdmin(ClarkGraduateFellowshipAdmin):

    model = GraduateFellowship

    def get_queryset(self, request):
        qs = get_queryset(self, request, GraduateFellowshipAdmin)
        return qs


class UndergraduateAdmin(GenericAdmin):
    """
    base admin class for the various undergrad applications
    """

    def signed_certification_link(self, instance):
        return '<a href="{}" target="_blank">Signed Certification</a>'.format(
            instance.signed_certification.url
        )
    signed_certification_link.allow_tags = True
    signed_certification_link.short_description = "Signed Certification"

    def high_school_transcripts_link(self, instance):
        try:
            code ='<a href="{}" target="_blank">High School Transcripts</a>'.format(
                instance.high_school_transcripts.url
            )
        except:
            code = None
        return code
    high_school_transcripts_link.allow_tags = True
    high_school_transcripts_link.short_description = "High School Transcripts"

    def undergraduate_transcripts_link(self, instance):
        return '<a href="{}" target="_blank">Undergraduate Transcripts</a>'.format(
            instance.undergraduate_transcripts.url
        )
    undergraduate_transcripts_link.allow_tags = True
    undergraduate_transcripts_link.short_description = """
        Undergraduate Transcripts
    """

    def wsgc_advisor_recommendation_link(self, instance):
        try:
            code = '<a href="{}" target="_blank">WSGC Advisor Rec.</a>'.format(
                instance.wsgc_advisor_recommendation.url
            )
        except:
            code = None
        return code
    wsgc_advisor_recommendation_link.allow_tags = True
    wsgc_advisor_recommendation_link.short_description = """
        WSGC Advisor Recommendation
    """

    def recommendation_link(self, instance):
        try:
            code = '<a href="{}" target="_blank">Recommendation</a>'.format(
                instance.recommendation.url
            )
        except:
            code = None
        return code
    recommendation_link.allow_tags = True
    recommendation_link.short_description = "Recommendation"

    def get_queryset(self, request):
        qs = get_queryset(self, request, UndergraduateAdmin)
        return qs


class UndergraduateResearchAdmin(UndergraduateAdmin):

    model = UndergraduateResearch

    list_display  = PROFILE_LIST_DISPLAY + [
        'project_title', 'begin_date', 'end_date',
        'funds_requested','funds_authorized',
        'other_funding', 'other_funding_explain',
        'synopsis_trunk','signed_certification_link','proposal_link',
        'high_school_transcripts_link','undergraduate_transcripts_link',
        'wsgc_advisor_recommendation_link','recommendation_link',
        'other_funding', 'other_funding_explain',
        'date_created','date_updated','status'
    ]
    list_editable = ['funds_authorized','status']
    list_display_links = ['project_title']
    actions = [export_longitudinal_tracking]

    def synopsis_trunk(self, instance):
        return Truncator(instance.synopsis).words(
            25, html=True, truncate=" ..."
        )
    synopsis_trunk.allow_tags = True
    synopsis_trunk.short_description = "Synopsis truncated"

    def proposal_link(self, instance):
        return '<a href="{}" target="_blank">Proposal</a>'.format(
            instance.proposal.url
        )
    proposal_link.allow_tags = True
    proposal_link.short_description = 'Proposal'

    def get_queryset(self, request):
        qs = get_queryset(self, request, UndergraduateResearchAdmin)
        return qs


class UndergraduateScholarshipAdmin(UndergraduateAdmin):

    model = UndergraduateScholarship

    list_display  = PROFILE_LIST_DISPLAY + [
        'signed_certification_link','statement_link',
        'high_school_transcripts_link','undergraduate_transcripts_link',
        'wsgc_advisor_recommendation_link','recommendation_link',
        'academic_institution',
        'other_funding', 'other_funding_explain',
        'date_created','date_updated','status'
    ]
    list_editable = ['status']
    actions = [export_longitudinal_tracking]

    def statement_link(self, instance):
        return '<a href="{}" target="_blank">Statement</a>'.format(
            instance.statement.url
        )
    statement_link.allow_tags = True
    statement_link.short_description = 'Statement'

    def get_queryset(self, request):
        qs = get_queryset(self, request, UndergraduateScholarshipAdmin)
        return qs


class StemBridgeScholarshipAdmin(UndergraduateScholarshipAdmin):

    model = StemBridgeScholarship

    def get_queryset(self, request):
        qs = get_queryset(self, request, StemBridgeScholarshipAdmin)
        return qs


class RocketLaunchTeamAdmin(GenericAdmin):

    model = RocketLaunchTeam

    list_display  = PROFILE_LIST_DISPLAY + [
        'name','academic_institution_name','competition','leader',
        'industry_mentor_name','industry_mentor_email',
        'date_created','date_updated',
        'wsgc_acknowledgement_link','budget_link','status'
    ]
    list_display_links = ['name']
    list_editable = ['status']
    raw_id_fields = ("user","leader","members",)

    def wsgc_acknowledgement_link(self, instance):
        if instance.wsgc_acknowledgement:
            return '<a href="{}" target="_blank">WSGC Acknowledgement</a>'.format(
                instance.wsgc_acknowledgement.url
            )
        else:
            return None

    wsgc_acknowledgement_link.allow_tags = True
    wsgc_acknowledgement_link.short_description = "WSGC Acknowledgement"

    def budget_link(self, instance):
        if instance.budget:
            return '<a href="{}" target="_blank">Budget</a>'.format(
                instance.budget.url
            )
        else:
            return None
    budget_link.allow_tags = True
    budget_link.short_description = "Budget"

    def get_queryset(self, request):
        qs = get_queryset(self, request, RocketLaunchTeamAdmin)
        return qs


class CollegiateRocketCompetitionAdmin(GenericAdmin):

    model = CollegiateRocketCompetition

    list_display  = PROFILE_LIST_DISPLAY + [
        'team','date_created','date_updated','cv_link','status'
    ]
    list_display_links = ['team']
    list_editable = ['status']
    actions = [export_longitudinal_tracking]

    def cv_link(self, instance):
        return '<a href="{}" target="_blank">CV</a>'.format(
            instance.cv.url
        )
    cv_link.allow_tags = True
    cv_link.short_description = "CV"

    def get_queryset(self, request):
        qs = get_queryset(self, request, CollegiateRocketCompetitionAdmin)
        return qs


class MidwestHighPoweredRocketCompetitionAdmin(GenericAdmin):

    model = MidwestHighPoweredRocketCompetition

    list_display  = PROFILE_LIST_DISPLAY + [
        'team','date_created','date_updated','cv_link','status'
    ]
    list_display_links = ['team']
    list_editable = ['status']
    actions = [export_longitudinal_tracking]

    def cv_link(self, instance):
        return '<a href="{}" target="_blank">CV</a>'.format(
            instance.cv.url
        )
    cv_link.allow_tags = True
    cv_link.short_description = "CV"

    def get_queryset(self, request):
        qs = get_queryset(self, request, MidwestHighPoweredRocketCompetitionAdmin)
        return qs


class FirstNationsRocketCompetitionAdmin(GenericAdmin):

    model = FirstNationsRocketCompetition

    list_display  = PROFILE_LIST_DISPLAY + [
        'team','date_created','date_updated','status'
    ]
    list_display_links = ['team']
    list_editable = ['status']
    actions = [export_longitudinal_tracking]

    def get_queryset(self, request):
        qs = get_queryset(self, request, FirstNationsRocketCompetitionAdmin)
        return qs


class HigherEducationInitiativesAdmin(GenericAdmin):

    model = HigherEducationInitiatives

    list_display  = PROFILE_LIST_DISPLAY + [
        'project_title', 'begin_date', 'end_date', 'award_type',
        'funds_requested', 'funds_authorized',
        'proposed_match', 'authorized_match', 'source_match', 'location',
        'synopsis_trunk', 'proposal_link',
        'finance_officer_name', 'finance_officer_address',
        'finance_officer_email', 'finance_officer_phone',
        'grant_officer_name','grant_officer_address',
        'grant_officer_email','grant_officer_phone',
        'date_created','date_updated','status'
    ]
    list_editable = ['funds_authorized','authorized_match', 'status']
    list_display_links = ['project_title']
    actions = [export_longitudinal_tracking]

    def synopsis_trunk(self, instance):
        return Truncator(instance.synopsis).words(
            25, html=True, truncate=" ..."
        )
    synopsis_trunk.allow_tags = True
    synopsis_trunk.short_description = "Synopsis truncated"

    def proposal_link(self, instance):
        return '<a href="{}" target="_blank">Proposal</a>'.format(
            instance.proposal.url
        )
    proposal_link.allow_tags = True
    proposal_link.short_description = 'Proposal file'

    def get_queryset(self, request):
        qs = get_queryset(self, request, HigherEducationInitiativesAdmin)
        return qs


class ResearchInfrastructureAdmin(HigherEducationInitiativesAdmin):

    model = ResearchInfrastructure

    def get_queryset(self, request):
        qs = get_queryset(self, request, ResearchInfrastructureAdmin)
        return qs


class AerospaceOutreachAdmin(HigherEducationInitiativesAdmin):

    model = AerospaceOutreach

    list_display  = PROFILE_LIST_DISPLAY + [
        'project_title', 'begin_date', 'end_date', 'project_category',
        'funds_requested', 'funds_authorized',
        'other_funding', 'other_funding_explain',
        'proposed_match', 'authorized_match', 'source_match', 'location',
        'synopsis_trunk', 'proposal_link',
        'finance_officer_name', 'finance_officer_address',
        'finance_officer_email', 'finance_officer_phone',
        'grant_officer_name','grant_officer_address',
        'grant_officer_email','grant_officer_phone',
        'date_created','date_updated','status'
    ]

    def get_queryset(self, request):
        qs = get_queryset(self, request, AerospaceOutreachAdmin)
        return qs


class NasaCompetitionAdmin(GenericAdmin):

    model = NasaCompetition

    list_display  = PROFILE_LIST_DISPLAY + [
        "competition_type", "competition_type_other",
        "facility_name", "facility_name_other",
        "program_acceptance", "award_type",
        'begin_date', 'end_date', 'funds_requested', 'funds_authorized',
        'proposed_match', 'authorized_match', 'source_match',
        'statement_link', 'budget_link',
        'finance_officer_name', 'finance_officer_address',
        'finance_officer_email', 'finance_officer_phone',
        'grant_officer_name','grant_officer_address',
        'grant_officer_email','grant_officer_phone',
        'date_created','date_updated','status'
    ]
    list_display_links = ['date_created']
    list_editable = ['status']
    #date_created.short_description = 'Created (edit)'
    actions = [export_longitudinal_tracking]

    def budget_link(self, instance):
        if instance.budget:
            return '<a href="{}" target="_blank">Budget</a>'.format(
                instance.budget.url
            )
        else:
            return None
    budget_link.allow_tags = True
    budget_link.short_description = "Budget"

    def statement_link(self, instance):
        return '<a href="{}" target="_blank">Statement</a>'.format(
            instance.statement.url
        )
    statement_link.allow_tags = True
    statement_link.short_description = 'Statement'

    def get_queryset(self, request):
        qs = get_queryset(self, request, NasaCompetitionAdmin)
        return qs


class SpecialInitiativesAdmin(AerospaceOutreachAdmin):

    model = SpecialInitiatives

    def get_queryset(self, request):
        qs = get_queryset(self, request, SpecialInitiativesAdmin)
        return qs


class WorkPlanTaskInline(admin.TabularInline):
    model = WorkPlanTask
    fields = ('title', 'description', 'hours_percent','expected_outcome')


class IndustryInternshipAdmin(GenericAdmin):

    list_display  = PROFILE_LIST_DISPLAY + [
        'award_type',
        'funds_requested', 'funds_authorized',
        'proposed_match', 'authorized_match', 'source_match',
        'date_created','date_updated','status'
    ]

    model = IndustryInternship
    list_display_links = ['first_name']
    list_editable = ['status']

    inlines = [WorkPlanTaskInline,]

    def get_queryset(self, request):
        qs = get_queryset(self, request, IndustryInternshipAdmin)
        return qs

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
'''
admin.site.register(
    WorkPlanTask, WorkPlanTaskAdmin
)
'''
