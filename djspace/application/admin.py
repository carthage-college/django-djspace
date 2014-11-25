from django.contrib import admin
from django.utils.text import Truncator

from djspace.application.models import *
from djspace.core.admin import GenericAdmin

class HighAltitudeBalloonLaunchAdmin(GenericAdmin):

    model = HighAltitudeBalloonLaunch

    list_display  = (
        'last_name', 'first_name', 'date_created','date_updated',
        'email_link', 'phone', 'cv_link', 'letter_interest_link', 'status'
    )

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

    def save_model(self, request, obj, form, change):
        obj.updated_by = request.user
        obj.save()

class ClarkGraduateFellowshipAdmin(GenericAdmin):

    model = ClarkGraduateFellowship

    list_display  = (
        'last_name', 'first_name', 'project_title', 'time_frame',
        'anticipating_funding', 'funds_requested', 'funds_authorized',
        'synopsis_trunk', 'signed_certification_link', 'proposal_link',
        'cv_link', 'budget_link', 'undergraduate_transcripts_link',
        'graduate_transcripts_link', 'recommendation_1_link',
        'recommendation_2_link', 'date_created','date_updated','status'
    )

    def synopsis_trunk(self, instance):
        return Truncator(instance.synopsis).words(25, html=True, truncate=" ...")
    synopsis_trunk.allow_tags = True

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
        return '<a href="{}" target="_blank">Undergrad Trans.</a>'.format(
            instance.undergraduate_transcripts.url
        )
    undergraduate_transcripts_link.allow_tags = True
    undergraduate_transcripts_link.short_description = "Undergrad Transcripts"

    def graduate_transcripts_link(self, instance):
        return '<a href="{}" target="_blank">Graduate Trans.</a>'.format(
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

    def save_model(self, request, obj, form, change):
        obj.updated_by = request.user
        obj.save()


class UndergraduateScholarshipAdmin(GenericAdmin):

    model = UndergraduateScholarship


class UndergraduateResearchAdmin(GenericAdmin):

    model = UndergraduateResearch


class FirstNationsLaunchCompetitionAdmin(GenericAdmin):

    model = FirstNationsLaunchCompetition

    list_display  = (
        'last_name', 'first_name', 'team_name', 'role',
        'date_created','date_updated', 'email_link',
        'phone', 'proposal_link', 'status'
    )

    def proposal_link(self, instance):
        return '<a href="{}" target="_blank">Proposal</a>'.format(
            instance.proposal.url
        )
    proposal_link.allow_tags = True
    proposal_link.short_description = 'Proposal file'



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
