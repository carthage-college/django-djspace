# -*- coding: utf-8 -*-

import csv

from django.contrib import admin
from django.urls import reverse
from django.http import HttpResponse
from django.urls import reverse
from django.utils.encoding import smart_str
from djspace.core.admin import PROFILE_LIST
from djspace.core.admin import GenericAdmin
from djspace.registration.models import *


PROFILE_HEADERS = [
    'Salutation',
    'First Name',
    'Second Name',
    'Last Name',
    'Email',
    'Email auxiliary',
    'Phone Primary',
    'Phone Mobile',
    'Permanent Address 1',
    'Address 2',
    'City',
    'State',
    'Postal Code',
    'Current Address 1',
    'Address 2',
    'City',
    'State',
    'Postal Code',
    'Date of Birth',
    'Gender',
    'Race',
    'Tribe',
    'Disability',
    'Disability Specifics',
    'Employment',
    'Military',
    'U.S. Citizen',
    'Registration Type',
    'WSGC Affiliate',
]


def get_profile_fields(registrant):
    """Obtain the fields for the Profile data model."""
    reg = registrant.user
    try:
        affiliate = reg.profile.get_registration().wsgc_affiliate
        if not affiliate:
            affiliate = reg.profile.get_registration().wsgc_affiliate_other
    except Except:
        affiliate = None

    race = [raza.name for raza in reg.profile.race.all()]
    return [
        reg.profile.salutation,
        smart_str(
            reg.first_name,
            encoding='utf-8',
            strings_only=False,
            errors='strict',
        ),
        smart_str(
            reg.profile.second_name,
            encoding='utf-8',
            strings_only=False,
            errors='strict',
        ),
        smart_str(
            reg.last_name,
            encoding='utf-8',
            strings_only=False,
            errors='strict',
        ),
        reg.email,
        reg.profile.email_auxiliary(),
        reg.profile.phone_primary,
        reg.profile.phone_mobile,
        reg.profile.address1,
        reg.profile.address2,
        reg.profile.city,
        reg.profile.state,
        reg.profile.postal_code,
        reg.profile.address1_current,
        reg.profile.address2_current,
        reg.profile.city_current,
        reg.profile.state_current,
        reg.profile.postal_code_current,
        reg.profile.date_of_birth,
        reg.profile.gender,
        ' '.join(race),
        smart_str(
            reg.profile.tribe,
            encoding='utf-8',
            strings_only=False,
            errors='strict',
        ),
        reg.profile.disability,
        reg.profile.disability_specify,
        reg.profile.employment,
        reg.profile.military,
        reg.profile.us_citizen,
        reg.profile.registration_type,
        affiliate,
    ]


def export_registrants(modeladmin, request, queryset):
    """Export registration data to CSV."""
    exclude = [
        'user',
        'user_id',
        'updated_by',
        'updated_by_id',
        'id',
        'date_created',
        'date_updated',
        'wsgc_affiliate_id',
        'wsgc_affiliate_id',
    ]
    response = HttpResponse('', content_type='text/csv; charset=utf-8')
    filename = '{0}.csv'.format(modeladmin)
    response['Content-Disposition'] = 'attachment; filename={0}'.format(filename)
    writer = csv.writer(response)
    field_names = [field.name for field in modeladmin.model._meta.get_fields()]
    headers = PROFILE_HEADERS[0:-1] + field_names
    # remove unwanted headers
    for ex in exclude:
        if ex in headers:
            headers.remove(ex)
    writer.writerow(headers)

    for reg in queryset:
        fields = get_profile_fields(reg)
        del fields[-1]
        for field in field_names:
            if field not in exclude:
                try:
                    field_val = getattr(reg, field, None)
                except Exception:
                    field_val = ''
                fields.append(field_val)
        writer.writerow(fields)
    return response


export_registrants.short_description = "Export Registrants"


class UndergraduateAdmin(GenericAdmin):
    """Undergraduate Admin model."""

    model = Undergraduate
    actions = [export_registrants]
    list_display = PROFILE_LIST
    list_filter = ()

    def last_name(self, instance):
        """Construct the link to the print view."""
        return mark_safe('<a href="{0}">{1}</a>'.format(
            reverse('registration_print', args=[instance.user.id]),
            instance.user.last_name,
        ))
    last_name.allow_tags = True
    last_name.short_description = 'Last Name (print)'

    def first_name(self, instance):
        """Return the user's first name."""
        return instance.user.first_name


class GraduateAdmin(UndergraduateAdmin):
    """Graduate Admin model."""

    model = Graduate


class FacultyAdmin(UndergraduateAdmin):
    """Faculty Admin model."""

    model = Faculty


class GrantsOfficerAdmin(UndergraduateAdmin):
    """Grants Officer Admin model."""

    model = GrantsOfficer


class HighSchoolAdmin(UndergraduateAdmin):
    """High School Admin model."""

    model = HighSchool


class ProfessionalAdmin(UndergraduateAdmin):
    """Professional Admin model."""

    model = Professional


admin.site.register(HighSchool, HighSchoolAdmin)
admin.site.register(Undergraduate, UndergraduateAdmin)
admin.site.register(Graduate, GraduateAdmin)
admin.site.register(Faculty, FacultyAdmin)
admin.site.register(GrantsOfficer, GrantsOfficerAdmin)
admin.site.register(Professional, ProfessionalAdmin)
