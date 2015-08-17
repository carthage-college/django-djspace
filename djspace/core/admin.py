from django import forms
from django.contrib import admin
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.contrib.auth.admin import UserAdmin

from djspace.core.models import UserProfile, GenericChoice
from djspace.core.utils import get_email_auxiliary

PROFILE_LIST_DISPLAY = [
    'salutation','first_name','second_name','last_name', 'email',
    'email_auxiliary', 'phone_primary','phone_mobile',
    'address1','address2','city','state','postal_code',
    'address1_current','address2_current', 'city_current','state_current',
    'postal_code_current','date_of_birth','gender','race','tribe',
    'disability','disability_specify','employment','military','us_citizen',
    'registration_type'
]

class GenericAdmin(admin.ModelAdmin):
    """
    Base admin class that represents the shared elements that
    most models can use, or override in their respective classes.
    """

    list_display = PROFILE_LIST_DISPLAY
    list_display_links = None

    date_hierarchy = 'date_created'
    ordering = [
        '-date_created','user__last_name','user__email'
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

    def phone_primary(self, obj):
        return obj.user.profile.phone_primary

    def phone_mobile(self, obj):
        return obj.user.profile.phone_mobile

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

    def address1_current(self, obj):
        return obj.user.profile.address1_current

    def address2_current(self, obj):
        return obj.user.profile.address2_current

    def city_current(self, obj):
        return obj.user.profile.city_current

    def state_current(self, obj):
        return obj.user.profile.state_current

    def postal_code_current(self, obj):
        return obj.user.profile.postal_code_current

    def gender(self, obj):
        return obj.user.profile.gender

    def disability(self, obj):
        return obj.user.profile.disability

    def disability_specify(self, obj):
        return obj.user.profile.disability_specify

    def us_citizen(self, obj):
        return obj.user.profile.us_citizen

    def employment(self, obj):
        return obj.user.profile.employment

    def military(self, obj):
        return obj.user.profile.military

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

    def email_auxiliary(self, obj):
        return get_email_auxiliary(obj)

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

    def save_model(self, request, obj, form, change):
        obj.updated_by = request.user
        obj.save()

admin.site.register(UserProfile, ProfileAdmin)

# override django admin user display
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    # we need this because UserProfile has two FK to auth.User model
    fk_name = 'user'

class UserProfileAdmin(UserAdmin):
    inlines = (UserProfileInline,)

admin.site.unregister(User)
admin.site.register(User, UserProfileAdmin)
