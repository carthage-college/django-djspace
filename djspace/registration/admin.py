from django.contrib import admin

from djspace.registration.models import *
from djspace.core.admin import GenericAdmin

class UndergraduateAdmin(GenericAdmin):

    model = Undergraduate
    list_per_page = 500
    raw_id_fields = ("user","updated_by",)


class GraduateAdmin(GenericAdmin):

    model = Graduate
    list_per_page = 500
    raw_id_fields = ("user","updated_by",)


class FacultyAdmin(GenericAdmin):

    model = Faculty
    list_per_page = 500
    raw_id_fields = ("user","updated_by",)


class ProfessionalAdmin(GenericAdmin):

    model = Professional
    list_per_page = 500
    raw_id_fields = ("user","updated_by",)


admin.site.register(Undergraduate, UndergraduateAdmin)
admin.site.register(Graduate, GraduateAdmin)
admin.site.register(Faculty, FacultyAdmin)
admin.site.register(Professional, ProfessionalAdmin)
