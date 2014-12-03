from django.contrib import admin

from djspace.registration.models import *
from djspace.core.admin import GenericAdmin

class UndergraduateAdmin(GenericAdmin):

    model = Undergraduate


class GraduateAdmin(GenericAdmin):

    model = Graduate


class FacultyAdmin(GenericAdmin):

    model = Faculty


class ProfessionalAdmin(GenericAdmin):

    model = Professional


admin.site.register(Undergraduate, UndergraduateAdmin)
admin.site.register(Graduate, GraduateAdmin)
admin.site.register(Faculty, FacultyAdmin)
admin.site.register(Professional, ProfessionalAdmin)
