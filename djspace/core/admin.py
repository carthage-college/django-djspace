from django import forms
from django.contrib import admin
from django.contrib import messages
from django.shortcuts import render
from django.template import RequestContext
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.admin import UserAdmin
from django.shortcuts import render_to_response
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
    'award_acceptance_file','interim_report_file','final_report_file'
]

POST_NO_OBJECTS = ['export_longitudinal_tracking']


import logging
logger = logging.getLogger(__name__)

class GenericAdmin(admin.ModelAdmin):
    """
    Base admin class that represents the shared elements that
    most models can use, or override in their respective classes.
    """

    change_form_template = 'admin/change_form.html'

    def get_urls(self):
        from django.conf.urls import patterns, url

        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)
            return update_wrapper(wrapper, view)

        info = self.model._meta.app_label, self.model._meta.model_name

        urls = patterns('',
            url(r'^(.+)/email/$',
                wrap(self.email_applicants),
                name='%s_%s_email' % info),
        )

        super_urls = super(GenericAdmin, self).get_urls()

        return urls + super_urls

    def email_applicants(self, request, queryset):
        action = queryset[0].status
        title = self.model._meta.verbose_name_plural
        logger.debug("outside POST logic")

        if 'action' in request.POST:
            form = EmailApplicantsForm(request.POST)
            if form.is_valid():
                form_data = form.cleaned_data
                sub = "WSGC: Information about your {} application".format(
                    title
                )
                '''
                send_mail (
                    request, TO_LIST, sub,
                    settings.SERVER_EMAIL, "admin/email_data.html",
                    data, BCC
                )
                '''
                messages.add_message(
                    request, messages.SUCCESS,
                    'The message was sent successfully.',
                    extra_tags='success'
                )
                self.message_user(request,'The message was sent successfully.')
                return HttpResponseRedirect(request.get_full_path())
        else:
            form = EmailApplicantsForm()

        return render_to_response (
            'admin/email_applicants.html', {
                'form': form,'action':action,'title':title,
                'objs':queryset
            },
            context_instance=RequestContext(request)
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
    list_filter   = ('status',)
    date_hierarchy = 'date_created'
    ordering = [
        'user__last_name','user__first_name'
    ]
    search_fields = (
        'user__last_name','user__first_name','user__email','user__username'
    )

    list_per_page = 500
    raw_id_fields = ("user","updated_by",)

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
        js = ('https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js',)

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
    last_name.short_description = 'Last Name (print)'

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

    def wsgc_affiliate(self, obj):
        return obj.user.profile.get_registration().wsgc_affiliate
    wsgc_affiliate.short_description = "Institution Name"

    def award_acceptance_file(self, instance):
        return admin_display_file(instance, "award_acceptance")
    award_acceptance_file.allow_tags = True
    award_acceptance_file.short_description = "Award Accpt"

    def interim_report_file(self, instance):
        return admin_display_file(instance, "interim_report")
    interim_report_file.allow_tags = True
    interim_report_file.short_description = "Interim Rpt"

    def final_report_file(self, instance):
        return admin_display_file(instance, "final_report")
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
