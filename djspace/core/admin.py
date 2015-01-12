from django import forms
from django.contrib import admin
from django.http import HttpResponse
from django.utils.encoding import smart_str
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.forms.models import model_to_dict
from django.contrib.auth.admin import UserAdmin

from djspace.core.models import UserProfile, GenericChoice

import csv

PROFILE_HEADERS = [
    'Salutation','First Name','Second Name','Last Name','Email','Phone',
    'Address 1','Address 2','City','State','Postal Code','Date of Birth',
    'Gender','Race','Tribe','Disability','U.S. Citizen','Registration Type'
]

def get_profile_fields(reg):
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
        reg.email,reg.profile.phone,reg.profile.address1,
        reg.profile.address2,reg.profile.city,reg.profile.state,
        reg.profile.postal_code,reg.profile.date_of_birth,
        reg.profile.gender,' '.join(race),reg.profile.tribe,
        reg.profile.disability,reg.profile.us_citizen,
        reg.profile.registration_type
    ]
    return fields

def export_registrants(modeladmin, request, queryset):
    # exclude these fields from registration data
    exclude = ['id','user']
    response = HttpResponse("", content_type="text/csv; charset=utf-8")
    filename = "{}.csv".format(modeladmin)
    response['Content-Disposition']='attachment; filename={}'.format(filename)
    writer = csv.writer(response)
    writer.writerow(PROFILE_HEADERS)
    for reg in queryset:
        fields = get_profile_fields(reg)
        reg_data = reg.profile.get_registration()
        if reg_data:
            for n,v in model_to_dict(reg_data).items():
                if n not in exclude:
                    fields.append(v)
        writer.writerow(fields)
    return response

export_registrants.short_description = "Export Registrants"

PROFILE_LIST_DISPLAY = [
    'salutation','first_name','second_name','last_name',
    'email','phone','address1','address2','city','state',
    'postal_code','date_of_birth','gender','race','tribe',
    'disability','us_citizen','registration_type'
]

class GenericAdmin(admin.ModelAdmin):
    """
    Base admin class that represents the shared elements that
    most models can use, or override in their respective classes.
    """

    list_display = PROFILE_LIST_DISPLAY
    list_display_links = None

    ordering = [
        'date_created','user__last_name','user__email'
    ]

    list_per_page = 500
    raw_id_fields = ("user","updated_by",)

    # user/profile data
    salutation =  lambda s, o: o.user.profile.salutation

    def first_name(self, obj):
        return obj.user.first_name

    def second_name(self, obj):
        return obj.user.profile.second_name

    def last_name(self, obj):
        return obj.user.last_name

    def phone(self, obj):
        return obj.user.profile.phone

    def address1(self, obj):
        return obj.user.profile.address1

    def address2(self, obj):
        return obj.user.profile.address2

    def city(self, obj):
        return obj.user.profile.city

    def state(self, obj):
        return obj.user.profile.state

    def postal_code(self, obj):
        return obj.user.profile.postal_code

    def gender(self, obj):
        return obj.user.profile.gender

    def disability(self, obj):
        return obj.user.profile.disability

    def us_citizen(self, obj):
        return obj.user.profile.us_citizen

    def race(self, obj):
        return "/".join([r.name for r in obj.user.profile.race.all()])

    def tribe(self, obj):
        return obj.user.profile.tribe

    def email(self, obj):
        return '<a href="%s">%s</a>' % (
            reverse("admin:auth_user_change", args=(obj.user.id,)),
            obj.user.email
        )
    email.allow_tags = True
    email.short_description = 'Profile (view/edit)'

    def registration_type(self, obj):
        try:
            reg_type = '<a href="%s">%s</a>' % (
                reverse(
                    "admin:registration_{}_change".format(
                        obj.user.profile.registration_type.lower()
                    ),
                    args=(obj.user.profile.get_registration().id,)
                ),
                obj.user.profile.registration_type
            )
        except:
            return None
        return reg_type
    registration_type.allow_tags = True
    registration_type.short_description = 'Reg Type (view/edit)'


    def date_of_birth(self, obj):
        return obj.user.profile.date_of_birth

    def save_model(self, request, obj, form, change):
        obj.updated_by = request.user
        obj.save()


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
