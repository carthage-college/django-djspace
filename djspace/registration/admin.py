from django.contrib import admin
from django.http import HttpResponse
from django.utils.encoding import smart_str
from django.core.urlresolvers import reverse
from django.forms.models import model_to_dict

from djspace.core.admin import GenericAdmin, PROFILE_LIST
from djspace.registration.models import *

import csv

PROFILE_HEADERS = [
    'Salutation','First Name','Second Name','Last Name',
    'Email', 'Email auxiliary', 'Phone Primary', 'Phone Mobile',
    'Permanent Address 1','Address 2','City','State','Postal Code',
    'Current Address 1','Address 2','City','State','Postal Code',
    'Date of Birth', 'Gender','Race','Tribe',
    'Disability','Disability Specifics', 'Employment','Military',
    'U.S. Citizen','Registration Type','WSGC Affiliate'
]


def get_profile_fields(obj):
    reg = obj.user
    affiliate =  reg.profile.get_registration().wsgc_affiliate
    if not affiliate:
        affiliate =  reg.profile.get_registration().wsgc_affiliate_other
    race = [r.name for r in reg.profile.race.all()]
    fields = [
        reg.profile.salutation,
        smart_str(
            reg.first_name,
            encoding='utf-8', strings_only=False, errors='strict'
        ),
        smart_str(
            reg.profile.second_name,
            encoding='utf-8', strings_only=False, errors='strict'
        ),
        smart_str(
            reg.last_name,
            encoding='utf-8', strings_only=False, errors='strict'
        ),
        reg.email,reg.profile.email_auxiliary(),
        reg.profile.phone_primary,reg.profile.phone_mobile,
        reg.profile.address1,reg.profile.address2,reg.profile.city,
        reg.profile.state,reg.profile.postal_code,
        reg.profile.address1_current,reg.profile.address2_current,
        reg.profile.city_current,reg.profile.state_current,
        reg.profile.postal_code_current,
        reg.profile.date_of_birth,reg.profile.gender,
        ' '.join(race),reg.profile.tribe,
        reg.profile.disability,reg.profile.disability_specify,
        reg.profile.employment,reg.profile.military,reg.profile.us_citizen,
        reg.profile.registration_type, affiliate
    ]
    return fields


def export_registrants(modeladmin, request, queryset):
    """
    Export registration data to CSV
    """
    exclude = [
        "user", "user_id", "updated_by", "updated_by_id", "id",
        "date_created", "date_updated", "wsgc_affiliate_id",
        "wsgc_affiliate_id"
    ]
    response = HttpResponse("", content_type="text/csv; charset=utf-8")
    filename = "{}.csv".format(modeladmin)
    response['Content-Disposition']='attachment; filename={}'.format(filename)
    writer = csv.writer(response)
    field_names = [f.name for f in modeladmin.model._meta.get_fields()]
    headers = PROFILE_HEADERS[0:-1] + field_names
    # remove unwanted headers
    for e in exclude:
        if e in headers:
            headers.remove(e)
    writer.writerow(headers)

    for reg in queryset:
        fields = get_profile_fields(reg)
        del fields[-1]
        for field in field_names:
            if field not in exclude:
                try:
                    val = unicode(
                        getattr(reg, field, None)
                    ).encode("utf-8", "ignore")
                except:
                    val = ''
                fields.append(val)
        writer.writerow(fields)
    return response

export_registrants.short_description = "Export Registrants"


class UndergraduateAdmin(GenericAdmin):

    model = Undergraduate
    actions = [export_registrants]
    list_display = PROFILE_LIST
    list_filter   = ()

    def last_name(self, obj):
        return u'<a href="{}">{}</a>'.format(
            reverse("registration_print", args=[obj.user.id]),
            obj.user.last_name
        )
    last_name.allow_tags = True
    last_name.short_description = 'Last Name (print)'


class GraduateAdmin(GenericAdmin):

    model = Graduate
    actions = [export_registrants]
    list_display = PROFILE_LIST
    list_filter   = ()

    def last_name(self, obj):
        return u'<a href="{}">{}</a>'.format(
            reverse("registration_print", args=[obj.user.id]),
            obj.user.last_name
        )
    last_name.allow_tags = True
    last_name.short_description = 'Last Name (print)'


class FacultyAdmin(GenericAdmin):

    model = Faculty
    actions = [export_registrants]
    list_display = PROFILE_LIST
    list_filter   = ()

    def last_name(self, obj):
        return u'<a href="{}">{}</a>'.format(
            reverse("registration_print", args=[obj.user.id]),
            obj.user.last_name
        )
    last_name.allow_tags = True
    last_name.short_description = 'Last Name (print)'


class ProfessionalAdmin(GenericAdmin):

    model = Professional
    actions = [export_registrants]
    list_display = PROFILE_LIST
    list_filter   = ()

    def last_name(self, obj):
        return u'<a href="{}">{}</a>'.format(
            reverse("registration_print", args=[obj.user.id]),
            obj.user.last_name
        )
    last_name.allow_tags = True
    last_name.short_description = 'Last Name (print)'


admin.site.register(Undergraduate, UndergraduateAdmin)
admin.site.register(Graduate, GraduateAdmin)
admin.site.register(Faculty, FacultyAdmin)
admin.site.register(Professional, ProfessionalAdmin)
