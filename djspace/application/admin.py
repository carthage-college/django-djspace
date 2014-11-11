from django.contrib import admin

from djspace.application.models import *
from djspace.core.admin import GenericAdmin

class HighAltitudeBalloonLaunchAdmin(GenericAdmin):

    model = HighAltitudeBalloonLaunch

    list_display  = (
        'last_name', 'first_name', 'date_created','date_updated',
        'email_link', 'phone', 'cv_link', 'letter_interest_link', 'status'
    )

    def __init__(self, *args, **kwargs):
        super(HighAltitudeBalloonLaunchAdmin, self).__init__(*args, **kwargs)
        self.list_display_links = (None, )

    def cv_link(self, instance):
        return "<a href='%s'>CV</a>" % (instance.cv.url,)
    cv_link.allow_tags = True
    cv_link.short_description = 'CV'

    def letter_interest_link(self, instance):
        return "<a href='%s'>Letter</a>" % (instance.letter_interest.url,)
    letter_interest_link.allow_tags = True
    letter_interest_link.short_description = 'Letter of interest'

    def save_model(self, request, obj, form, change):
        obj.updated_by = request.user
        super(HighAltitudeBalloonLaunchAdmin, self).save(
            request, obj, form, change
        )

class HighAltitudeBalloonPayloadAdmin(HighAltitudeBalloonLaunchAdmin):

    model = HighAltitudeBalloonPayload

    def __init__(self, *args, **kwargs):
        super(HighAltitudeBalloonPayloadAdmin, self).__init__(*args, **kwargs)
        self.list_display_links = (None, )

    def save_model(self, request, obj, form, change):
        obj.updated_by = request.user
        super(HighAltitudeBalloonPayloadAdmin, self).save(
            request, obj, form, change
        )

class ClarkGraduateFellowshipAdmin(GenericAdmin):

    model = ClarkGraduateFellowship

    def save_model(self, request, obj, form, change):
        obj.updated_by = request.user
        super(ClarkGraduateFellowshipAdmin, self).save(
            request, obj, form, change
        )

class GraduateFellowshipAdmin(ClarkGraduateFellowshipAdmin):

    model = GraduateFellowship

    def save_model(self, request, obj, form, change):
        obj.updated_by = request.user
        super(GraduateFellowshipAdmin, self).save(
            request, obj, form, change
        )

class UndergraduateScholarshipAdmin(GenericAdmin):

    model = UndergraduateScholarship

    def save_model(self, request, obj, form, change):
        obj.updated_by = request.user
        super(UndergraduateScholarship, self).save(
            request, obj, form, change
        )

class UndergraduateResearchAdmin(GenericAdmin):

    model = UndergraduateResearch

    def save_model(self, request, obj, form, change):
        obj.updated_by = request.user
        super(UndergraduateResearch, self).save(
            request, obj, form, change
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
