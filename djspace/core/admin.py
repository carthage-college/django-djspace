from django import forms
from django.contrib import admin
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.forms.models import model_to_dict
from django.contrib.auth.admin import UserAdmin

from djspace.core.models import UserProfile, GenericChoice

import csv

def export_registrants(modeladmin, request, queryset):
    # exclude these fields from registration data
    exclude = ['id','user']
    response = HttpResponse("", content_type="text/csv; charset=utf-8")
    response['Content-Disposition']='attachment; filename=wsgc_registrants.csv'
    writer = csv.writer(response)
    writer.writerow([
        'Salutation','First Name','Second Name','Last Name','Email','Phone',
        'Address 1','Address 2','City','State','Postal Code','Date of Birth',
        'Gender','Race','Tribe','Disability','U.S. Citizen','Registration Type'
    ])
    for reg in queryset:
        race = [r.name for r in reg.profile.race.all()]
        fields = [
            reg.profile.salutation,reg.first_name,reg.profile.second_name,
            reg.last_name,reg.email,reg.profile.phone,reg.profile.address1,
            reg.profile.address2,reg.profile.city,reg.profile.state,
            reg.profile.postal_code,reg.profile.date_of_birth,
            reg.profile.gender,' '.join(race),reg.profile.tribe,
            reg.profile.disability,reg.profile.us_citizen,
            reg.profile.registration_type
        ]
        reg_data = reg.profile.get_registration()
        if reg_data:
            for n,v in model_to_dict(reg_data).items():
                if n not in exclude:
                    fields.append(v)
        writer.writerow(fields)
    return response

export_registrants.short_description = "Export Registrants"

class GenericAdmin(admin.ModelAdmin):

    list_display  = (
        'last_name', 'first_name', 'email_link', 'phone',
        'date_created', 'date_updated',
    )

    ordering = [
        'date_created','user__last_name','user__email'
    ]

    list_per_page = 500
    raw_id_fields = ("user","updated_by",)

    def first_name(self, obj):
        return obj.user.first_name

    def last_name(self, obj):
        return obj.user.last_name

    def email_link(self, obj):
        return "<a href='%s'>%s</a>" % (
            reverse('admin:auth_user_change', args=(obj.user.id,)),
            obj.user.email
        )
    email_link.allow_tags = True
    email_link.short_description = 'User Profile'

    def phone(self, obj):
        return obj.user.profile.phone

class GenericChoiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'value', 'ranking', 'active', 'tags')

admin.site.register(GenericChoice, GenericChoiceAdmin)

class ProfileAdmin(admin.ModelAdmin):
    search_fields = (
        'user__last_name','user__first_name','user__email','user__username'
    )

admin.site.register(UserProfile, ProfileAdmin)

# override django admin user display
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    # we need this because UserProfile has two FK to auth.User model
    fk_name = 'user'

class UserProfileAdmin(UserAdmin):
    inlines = (UserProfileInline,)
    actions = [export_registrants]

admin.site.unregister(User)
admin.site.register(User, UserProfileAdmin)
