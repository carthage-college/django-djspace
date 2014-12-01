from django.contrib import admin
from django.utils.text import Truncator

from djspace.application.models import *
from djspace.core.admin import GenericAdmin, PROFILE_LIST_DISPLAY

class HighAltitudeBalloonLaunchAdmin(GenericAdmin):

    model = HighAltitudeBalloonLaunch

    list_display  = PROFILE_LIST_DISPLAY + [
        'cv_link', 'letter_interest_link',
        'date_created','date_updated',
        'status'
    ]
    list_editable = ['status']

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


class HighAltitudeBalloonPayloadAdmin(HighAltitudeBalloonLaunchAdmin):

    model = HighAltitudeBalloonPayload


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

    def synopsis_trunk(self, instance):
        return Truncator(instance.synopsis).words(25, html=True, truncate=" ...")
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
        return '<a href="{}" target="_blank">Rec. 1</a>'.format(
            instance.recommendation_1.url
        )
    recommendation_1_link.allow_tags = True
    recommendation_1_link.short_description = "Recommendation 1"

    def recommendation_2_link(self, instance):
        return '<a href="{}" target="_blank">Rec. 2</a>'.format(
            instance.recommendation_2.url
        )
    recommendation_2_link.allow_tags = True
    recommendation_2_link.short_description = "Recommendation 2"


class GraduateFellowshipAdmin(ClarkGraduateFellowshipAdmin):

    model = GraduateFellowship


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

    def synopsis_trunk(self, instance):
        return Truncator(instance.synopsis).words(25,html=True,truncate="...")
    synopsis_trunk.allow_tags = True
    synopsis_trunk.short_description = "Synopsis truncated"

    def proposal_link(self, instance):
        return '<a href="{}" target="_blank">Proposal</a>'.format(
            instance.proposal.url
        )
    proposal_link.allow_tags = True
    proposal_link.short_description = 'Proposal'


class UndergraduateScholarshipAdmin(UndergraduateAdmin):

    model = UndergraduateScholarship

    list_display  = PROFILE_LIST_DISPLAY + [
        'signed_certification_link','statement_link',
        'high_school_transcripts_link','undergraduate_transcripts_link',
        'wsgc_advisor_recommendation_link','recommendation_link',
        'date_created','date_updated','status'
    ]

    def statement_link(self, instance):
        return '<a href="{}" target="_blank">Statement</a>'.format(
            instance.statement.url
        )
    statement_link.allow_tags = True
    statement_link.short_description = 'Statement'


class FirstNationsLaunchCompetitionAdmin(GenericAdmin):

    model = FirstNationsLaunchCompetition

    list_display  = PROFILE_LIST_DISPLAY + [
        'team_name','role','date_created','date_updated','proposal_link',
        'date_created','date_updated','status'
    ]
    list_editable = ['status']

    def proposal_link(self, instance):
        return '<a href="{}" target="_blank">Proposal</a>'.format(
            instance.proposal.url
        )
    proposal_link.allow_tags = True
    proposal_link.short_description = 'Proposal'

admin.site.register(
    FirstNationsLaunchCompetition, FirstNationsLaunchCompetitionAdmin
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
