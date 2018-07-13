from django import forms
from django.contrib import admin
from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.contrib.auth.admin import UserAdmin
from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.templatetags.admin_urls import add_preserved_filters

from djspace.core.forms import EmailApplicantsForm
from djspace.core.models import UserProfile, GenericChoice
from djspace.core.utils import admin_display_file, get_email_auxiliary

from functools import update_wrapper


# base list that all registration types and program applications can use
PROFILE_LIST = [
    'salutation','last_name','first_name','date_of_birth',
    'email','date_created','date_updated','registration_type',
    'email_auxiliary','phone_primary','phone_mobile',
    'address1','address2','city','state','postal_code',
    'address1_current','address2_current','city_current','state_current',
    'postal_code_current','gender','race','tribe',
    'disability','disability_specify','employment','military','us_citizen',
    'wsgc_affiliate',
]
# program applications all have the following fields in common
PROFILE_LIST_DISPLAY = PROFILE_LIST + [
    'mugshot_file','biography_file','media_release_file','irs_w9_file',
    'award_acceptance_file','interim_report_file','final_report_file'
]

POST_NO_OBJECTS = ['export_longitudinal_tracking']


class GenericAdmin(admin.ModelAdmin):
    """
    Base admin class that represents the shared elements that
    most models can use, or override in their respective classes.
    """

    def email_applicants(self, request, queryset):
        """
        admin action that displays a textarea for email input
        and then sends the data off to another view for sending
        of said email to all selected applicants
        """

        title = self.model._meta.verbose_name_plural
        form = EmailApplicantsForm()
        ct = ContentType.objects.get_for_model(queryset.model)

        return render (
            request, 'admin/email_applicants.html', {
                'form':form,'title':title,'objs':queryset,
                'content_type':ct.pk
            }
        )
    email_applicants.short_description = u'Email selected applicants'

    def changelist_view(self, request, extra_context=None):
        """
        Override the action form on the listing view so that we can
        submit the form without selecting any objects
        """
        if 'action' in request.POST and request.POST['action'] in POST_NO_OBJECTS:
            if not request.POST.getlist(admin.ACTION_CHECKBOX_NAME):
                post = request.POST.copy()
                post.update({admin.ACTION_CHECKBOX_NAME: str(1)})
                request._set_post(post)
        return super(GenericAdmin, self).changelist_view(
            request, extra_context
        )

    list_display = PROFILE_LIST_DISPLAY
    list_display_links = None
    #list_filter   = ('status','complete')
    date_hierarchy = 'date_created'
    ordering = [
        'user__last_name','user__first_name'
    ]
    search_fields = (
        'user__last_name','user__first_name','user__email','user__username'
    )

    list_per_page = 20
    raw_id_fields = ('user','updated_by',)

    # user/profile data
    salutation =  lambda s, o: o.user.profile.salutation

    class Media:
        css = {
             'all': (
                'https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css',
                'https://maxcdn.bootstrapcdn.com/font-awesome/4.6.3/css/font-awesome.min.css',
                '/static/djspace/css/admin.css'
            )
        }
        js = (
            'https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js',
            'https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js',
            'https://www.carthage.edu/static/vendor/jquery/plugins/jqDoubleScroll/jquery.doubleScroll.js',
            '/static/djspace/js/admin.js'
        )


    def first_name(self, obj):
        return obj.user.first_name

    def second_name(self, obj):
        return obj.user.profile.second_name

    def last_name(self, obj):
        return u'<a href="{}">{}</a>'.format(
            reverse("application_print", args=(obj.get_slug(),obj.id)),
            obj.user.last_name
        )
    last_name.allow_tags = True
    last_name.short_description = "Last Name (print)"

    def phone_primary(self, obj):
        return obj.user.profile.phone_primary

    def phone_mobile(self, obj):
        return obj.user.profile.phone_mobile

    def address1(self, obj):
        return obj.user.profile.address1
    address1.short_description = "Address1 permanent"

    def address2(self, obj):
        return obj.user.profile.address2
    address2.short_description = "Address2 permanent"

    def city(self, obj):
        return obj.user.profile.city
    city.short_description = "City permanent"

    def state(self, obj):
        return obj.user.profile.state
    state.short_description = "State permanent"

    def postal_code(self, obj):
        return obj.user.profile.postal_code
    postal_code.short_description = "Postal code permanent"

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

    def date_of_birth(self, obj):
        return obj.user.profile.date_of_birth

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
        return '<a href="mailto:{}">{}</a>'.format(
            obj.user.email, obj.user.email
        )
    email.allow_tags = True
    email.short_description = 'Email'

    def email_auxiliary(self, obj):
        return get_email_auxiliary(obj.user)

    def registration_type(self, obj):
        try:
            reg_type = '<a href="{}">{}</a>'.format(
                reverse(
                    'admin:registration_{}_change'.format(
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

    def wsgc_affiliate(self, obj):
        try:
            wsgc_affiliate = obj.user.profile.get_registration().wsgc_affiliate
        except:
            wsgc_affiliate = None
        return wsgc_affiliate
    wsgc_affiliate.short_description = "Institution Name"

    def mugshot_file(self, instance):
        try:
            return admin_display_file(instance.user.user_files, 'mugshot')
        except:
            return '<i class="fa fa-times-circle red" aria-hidden="true"></i>'
    mugshot_file.allow_tags = True
    mugshot_file.short_description = "Photo"

    def biography_file(self, instance):
        try:
            return admin_display_file(instance.user.user_files, 'biography')
        except:
            return '<i class="fa fa-times-circle red" aria-hidden="true"></i>'
    biography_file.allow_tags = True
    biography_file.short_description = "Bio"

    def media_release_file(self, instance):
        try:
            return admin_display_file(instance.user.user_files, 'media_release')
        except:
            return '<i class="fa fa-times-circle red" aria-hidden="true"></i>'
    media_release_file.allow_tags = True
    media_release_file.short_description = "Media"

    def irs_w9_file(self, instance):
        try:
            return admin_display_file(instance.user.user_files, 'irs_w9')
        except:
            return '<i class="fa fa-times-circle red" aria-hidden="true"></i>'
    irs_w9_file.allow_tags = True
    irs_w9_file.short_description = "W9"

    def award_acceptance_file(self, instance):
        return admin_display_file(instance, 'award_acceptance')
    award_acceptance_file.allow_tags = True
    award_acceptance_file.short_description = "Award Accpt"

    def interim_report_file(self, instance):
        return admin_display_file(instance, 'interim_report')
    interim_report_file.allow_tags = True
    interim_report_file.short_description = "Interim Rpt"

    def final_report_file(self, instance):
        return admin_display_file(instance, 'final_report')
    final_report_file.allow_tags = True
    final_report_file.short_description = "Final Rpt"

    def save_model(self, request, obj, form, change):
        obj.updated_by = request.user
        obj.save()


class GenericChoiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'value', 'ranking', 'active')

admin.site.register(GenericChoice, GenericChoiceAdmin)

class ProfileAdmin(admin.ModelAdmin):

    list_display = [
        'last_name','first_name','email','username','id'
    ]

    ordering = [
        'user__last_name','user__first_name','id'
    ]
    search_fields = (
        'user__last_name','user__first_name',
        'user__email','user__username','user__id'
    )

    date_hierarchy = 'date_created'

    list_per_page = 500
    raw_id_fields = ("user","updated_by",)


    def last_name(self, instance):
        return instance.user.last_name

    def first_name(self, instance):
        return instance.user.first_name

    def email(self, instance):
        return instance.user.email

    def username(self, instance):
        return instance.user.username

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
