from django.contrib import admin

from djspace.registration.models import *
from djspace.core.admin import GenericAdmin

class UndergraduateAdmin(admin.ModelAdmin):

    model = Undergraduate


class GraduateAdmin(admin.ModelAdmin):

    model = Graduate


class FacultyAdmin(admin.ModelAdmin):

    model = Faculty


class ProfessionalAdmin(admin.ModelAdmin):

    model = Professional


admin.site.register(Undergraduate, UndergraduateAdmin)
admin.site.register(Graduate, GraduateAdmin)
admin.site.register(Faculty, FacultyAdmin)
admin.site.register(Professional, ProfessionalAdmin)
