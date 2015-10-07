# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib import admin
from django.http import HttpResponse
from django.utils.text import Truncator
from django.utils.html import strip_tags
from django.forms.models import model_to_dict

from djspace.application.models import *
from djspace.core.admin import GenericAdmin, PROFILE_LIST_DISPLAY
from djspace.registration.admin import PROFILE_HEADERS, get_profile_fields

import csv
import datetime

def get_queryset(self, request, admin_class):
    """
    only show applications that were created after a certain date.
    they wanted to see only applications for the current grant cycle.
    so we hide old applications.
    """
    TODAY = datetime.date.today()
    YEAR = int(TODAY.year)
    MES = int(TODAY.month)
    qs = super(admin_class, self).queryset(request)
    if MES < settings.GRANT_CYCLE_START_MES:
        YEAR = YEAR - 1
    start_date = datetime.date(YEAR, settings.GRANT_CYCLE_START_MES, 1)
    return qs.filter(date_created__gte=start_date)

def export_applications(modeladmin, request, queryset, reg_type=None):
    """
    Export application data to CSV
    """

    file_fields = [
        "cv", "proposal", "signed_certification", "letter_interest",
        "budget", "undergraduate_transcripts", "graduate_transcripts",
        "recommendation", "recommendation_1", "recommendation_2",
        "high_school_transcripts", "wsgc_advisor_recommendation",
        "statement"
    ]
    exclude = [
        "user", "user_id", "updated_by_id", "id",
        "aerospaceoutreach", "clarkgraduatefellowship",
        "firstnationsrocketcompetition", "graduatefellowship",
        "highaltitudeballoonpayload","highaltitudeballoonlaunch",
        "researchinfrastructure", "specialinitiatives",
        "undergraduateresearch", "undergraduatescholarship"
    ]
    response = HttpResponse("", content_type="text/csv; charset=utf-8")
    filename = "{}.csv".format(modeladmin)
    response['Content-Disposition']='attachment; filename={}'.format(filename)
    writer = csv.writer(response)
    headers = PROFILE_HEADERS + modeladmin.model._meta.get_all_field_names()
    # remove unwanted headers
    for e in exclude:
        if e in headers:
            headers.remove(e)

    writer.writerow(headers)
    for reg in queryset:
        #fields = get_profile_fields(reg.user)
        fields = get_profile_fields(reg)
        for field in reg._meta.get_all_field_names():
            if field not in exclude:
                if field == "synopsis":
                    val = unicode(strip_tags(getattr(reg, field, None))).encode("utf-8", "ignore").strip()
                else:
                    val = unicode(getattr(reg, field, None)).encode("utf-8", "ignore")
                if field in file_fields:
                    val = "https://{}{}{}".format(
                        settings.SERVER_URL, settings.MEDIA_URL,
                        getattr(reg, field, None)
                    )
                fields.append(val)
        writer.writerow(fields)
    return response

def export_all_applications(modeladmin, request, queryset):
    """
    Export application data to CSV for all registration types
    """

    return export_applications(modeladmin, request, queryset)

export_all_applications.short_description = "Export All Applications"


class HighAltitudeBalloonLaunchAdmin(GenericAdmin):

    model = HighAltitudeBalloonLaunch

    list_display  = PROFILE_LIST_DISPLAY + [
        'cv_link', 'letter_interest_link',
        'date_created','date_updated',
        'status'
    ]
    list_editable = ['status']
    actions = [export_all_applications]

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

    def queryset(self, request):
        qs = get_queryset(self, request, HighAltitudeBalloonLaunchAdmin)
        return qs


class HighAltitudeBalloonPayloadAdmin(HighAltitudeBalloonLaunchAdmin):

    model = HighAltitudeBalloonPayload

    def queryset(self, request):
        qs = get_queryset(self, request, HighAltitudeBalloonPayloadAdmin)
        return qs


class ClarkGraduateFellowshipAdmin(GenericAdmin):

    model = ClarkGraduateFellowship

    list_display  = PROFILE_LIST_DISPLAY + [
        'project_title', 'time_frame',
        'anticipating_funding', 'funds_requested', 'funds_authorized',
        'synopsis_trunk', 'signed_certification_link', 'proposal_link',
        'cv_link', 'budget_link', 'undergraduate_transcripts_link',
        'graduate_transcripts_link', 'recommendation_1_link',
        'recommendation_2_link', 'date_created','date_updated','status'
    ]
    list_editable = ['funds_authorized','status']
    list_display_links = ['project_title']
    actions = [export_all_applications]

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

    def queryset(self, request):
        qs = get_queryset(self, request, ClarkGraduateFellowshipAdmin)
        return qs


class GraduateFellowshipAdmin(ClarkGraduateFellowshipAdmin):

    model = GraduateFellowship

    def queryset(self, request):
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

    def queryset(self, request):
        qs = get_queryset(self, request, UndergraduateAdmin)
        return qs


class UndergraduateResearchAdmin(UndergraduateAdmin):

    model = UndergraduateResearch

    list_display  = PROFILE_LIST_DISPLAY + [
        'project_title','time_frame','funds_requested','funds_authorized',
        'synopsis_trunk','signed_certification_link','proposal_link',
        'high_school_transcripts_link','undergraduate_transcripts_link',
        'wsgc_advisor_recommendation_link','recommendation_link',
        'date_created','date_updated','status'
    ]
    list_editable = ['funds_authorized','status']
    list_display_links = ['project_title']
    actions = [export_all_applications]

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

    def queryset(self, request):
        qs = get_queryset(self, request, UndergraduateResearchAdmin)
        return qs


class UndergraduateScholarshipAdmin(UndergraduateAdmin):

    model = UndergraduateScholarship

    list_display  = PROFILE_LIST_DISPLAY + [
        'signed_certification_link','statement_link',
        'high_school_transcripts_link','undergraduate_transcripts_link',
        'wsgc_advisor_recommendation_link','recommendation_link',
        'date_created','date_updated','status'
    ]
    list_editable = ['status']
    actions = [export_all_applications]

    def statement_link(self, instance):
        return '<a href="{}" target="_blank">Statement</a>'.format(
            instance.statement.url
        )
    statement_link.allow_tags = True
    statement_link.short_description = 'Statement'

    def queryset(self, request):
        qs = get_queryset(self, request, UndergraduateScholarshipAdmin)
        return qs

class RocketLaunchTeamAdmin(GenericAdmin):

    model = RocketLaunchTeam

    list_display  = PROFILE_LIST_DISPLAY + [
        'name','academic_institution_name','leader',
        'industry_mentor_name','industry_mentor_email',
        'date_created','date_updated',
        'wsgc_acknowledgement_link','budget_link','tags','status'
    ]
    list_display_links = ['name']
    list_editable = ['status','tags']
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


class CollegiateRocketCompetitionAdmin(GenericAdmin):

    model = CollegiateRocketCompetition

    list_display  = PROFILE_LIST_DISPLAY + [
        'team','date_created','date_updated','cv_link','status'
    ]
    list_display_links = ['team']
    list_editable = ['status']
    actions = [export_all_applications]

    def cv_link(self, instance):
        return '<a href="{}" target="_blank">CV</a>'.format(
            instance.cv.url
        )
    cv_link.allow_tags = True
    cv_link.short_description = "CV"

    def queryset(self, request):
        qs = get_queryset(self, request, CollegiateRocketCompetitionAdmin)
        return qs


class MidwestHighPoweredRocketCompetitionAdmin(GenericAdmin):

    model = MidwestHighPoweredRocketCompetition

    list_display  = PROFILE_LIST_DISPLAY + [
        'team','date_created','date_updated','cv_link','status'
    ]
    list_display_links = ['team']
    list_editable = ['status']
    actions = [export_all_applications]

    def cv_link(self, instance):
        return '<a href="{}" target="_blank">CV</a>'.format(
            instance.cv.url
        )
    cv_link.allow_tags = True
    cv_link.short_description = "CV"

    def queryset(self, request):
        qs = get_queryset(self, request, MidwestHighPoweredRocketCompetitionAdmin)
        return qs


class FirstNationsRocketCompetitionAdmin(GenericAdmin):

    model = FirstNationsRocketCompetition

    list_display  = PROFILE_LIST_DISPLAY + [
        'team','date_created','date_updated','cv_link','status'
    ]
    list_display_links = ['team']
    list_editable = ['status']
    actions = [export_all_applications]

    def cv_link(self, instance):
        return '<a href="{}" target="_blank">CV</a>'.format(
            instance.cv.url
        )
    cv_link.allow_tags = True
    cv_link.short_description = "CV"

    def queryset(self, request):
        qs = get_queryset(self, request, FirstNationsRocketCompetitionAdmin)
        return qs


class HigherEducationInitiativesAdmin(GenericAdmin):

    model = HigherEducationInitiatives

    list_display  = PROFILE_LIST_DISPLAY + [
        'project_title', 'time_frame',
        'funds_requested', 'funds_authorized',
        'proposed_match', 'authorized_match', 'source_match', 'location',
        'synopsis_trunk', 'proposal_link',
        'date_created','date_updated','status'
    ]
    list_editable = ['funds_authorized','authorized_match', 'status']
    list_display_links = ['project_title']
    actions = [export_all_applications]

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

    def queryset(self, request):
        qs = get_queryset(self, request, HigherEducationInitiativesAdmin)
        return qs


class ResearchInfrastructureAdmin(HigherEducationInitiativesAdmin):

    model = ResearchInfrastructure

    def queryset(self, request):
        qs = get_queryset(self, request, ResearchInfrastructureAdmin)
        return qs


class AerospaceOutreachAdmin(HigherEducationInitiativesAdmin):

    model = AerospaceOutreach

    def queryset(self, request):
        qs = get_queryset(self, request, AerospaceOutreachAdmin)
        return qs


class SpecialInitiativesAdmin(HigherEducationInitiativesAdmin):

    model = SpecialInitiatives

    def queryset(self, request):
        qs = get_queryset(self, request, SpecialInitiativesAdmin)
        return qs


class IndustryInternshipAdmin(GenericAdmin):

    model = IndustryInternship


class WorkPlanTaskAdmin(admin.ModelAdmin):

    model = WorkPlanTask
    list_display = ['title']


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
    UndergraduateScholarship, UndergraduateScholarshipAdmin
)
admin.site.register(
    UndergraduateResearch, UndergraduateResearchAdmin
)
admin.site.register(
    IndustryInternship, IndustryInternshipAdmin
)
admin.site.register(
    WorkPlanTask, WorkPlanTaskAdmin
)
