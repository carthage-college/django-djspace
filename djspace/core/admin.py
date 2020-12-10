# -*- coding: utf-8 -*-

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.shortcuts import render
from djspace.core.forms import EmailApplicantsForm
from djspace.core.models import GenericChoice
from djspace.core.models import UserProfile
from djspace.core.utils import admin_display_file
from djspace.core.utils import get_email_auxiliary


# base list that all registration types and program applications can use
PROFILE_LIST = [
    'salutation',
    'last_name',
    'first_name',
    'date_of_birth',
    'email',
    'date_created',
    'date_updated',
    'registration_type',
    'email_auxiliary',
    'phone_primary',
    'phone_mobile',
    'address1',
    'address2',
    'city',
    'state',
    'postal_code',
    'address1_current',
    'address2_current',
    'city_current',
    'state_current',
    'postal_code_current',
    'gender',
    'race',
    'tribe',
    'disability',
    'disability_specify',
    'employment',
    'military',
    'us_citizen',
    'wsgc_affiliate',
]
# program applications all have the following fields in common
PROFILE_LIST_DISPLAY = PROFILE_LIST + [
    'mugshot_file',
    'biography_file',
    'media_release_file',
    'irs_w9_file',
    'award_acceptance_file',
    'interim_report_file',
    'final_report_file',
    'other_file_file',
    'other_file2_file',
    'other_file3_file',
]

POST_NO_OBJECTS = ['export_longitudinal_tracking']


class GenericAdmin(admin.ModelAdmin):
    """
    Base admin class.

    Represents the shared elements that most models can use,
    or override in their respective classes.
    """

    def email_applicants(self, request, queryset):
        """
        Admin action that displays a textarea for email input.

        Sends the data off to another view for sending
        of said email to all selected applicants
        """
        title = self.model._meta.verbose_name_plural
        form = EmailApplicantsForm()
        ct = ContentType.objects.get_for_model(queryset.model)

        return render(
            request,
            'admin/email_applicants.html',
            {
                'form': form, 'title': title, 'objs': queryset, 'content_type': ct.pk,
            },
        )
    email_applicants.short_description = 'Email selected applicants'

    def changelist_view(self, request, extra_context=None):
        """
        Override the action form on the listing view.

        We can then submit the form without selecting any objects.
        """
        if 'action' in request.POST and request.POST['action'] in POST_NO_OBJECTS:
            if not request.POST.getlist(admin.ACTION_CHECKBOX_NAME):
                post = request.POST.copy()
                post.update({admin.ACTION_CHECKBOX_NAME: str(1)})
                request._set_post(post)
        return super(GenericAdmin, self).changelist_view(request, extra_context)

    list_display = PROFILE_LIST_DISPLAY
    list_display_links = None
    date_hierarchy = 'date_created'
    ordering = ['user__last_name', 'user__first_name']
    search_fields = (
        'user__last_name', 'user__first_name', 'user__email', 'user__username',
    )

    list_per_page = 20
    raw_id_fields = ('user', 'updated_by')
    salutation = lambda s, o: o.user.profile.salutation

    class Media:
        """Inject static files into the admin view."""

        css = {
            'all': (
                '//maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css',
                '//maxcdn.bootstrapcdn.com/font-awesome/4.6.3/css/font-awesome.min.css',
                '/static/djspace/css/admin.css',
            ),
        }
        js = (
            'https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js',
            'https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js',
            '//www.carthage.edu/static/vendor/jquery/plugins/jqDoubleScroll/jquery.doubleScroll.js',
            '/static/djspace/js/admin.js',
        )

    def second_name(self, instance):
        """Return the user's second name."""
        return instance.user.profile.second_name

    def last_name(self, instance):
        """Construct the link to the print view using the user's last name."""
        return '<a href="{0}" target="_blank">{1}</a>'.format(
            reverse("application_print", args=(instance.get_slug(), instance.id)),
            instance.user.last_name,
        )
    last_name.allow_tags = True
    last_name.short_description = "Last Name (print)"

    def first_name(self, instance):
        """Construct the link to the default view using the user's first name."""
        return '<a href="{0}" target="_blank">{1}</a>'.format(
            instance.get_absolute_url(), instance.user.first_name,
        )
    first_name.allow_tags = True
    first_name.short_description = "Given Name (edit)"

    def phone_primary(self, instance):
        """Return the user's primary phone number."""
        return instance.user.profile.phone_primary

    def phone_mobile(self, instance):
        """Return the user's mobile phone number."""
        return instance.user.profile.phone_mobile

    def address1(self, instance):
        """Return the user's permanent address."""
        return instance.user.profile.address1
    address1.short_description = "Address1 permanent"

    def address2(self, instance):
        """Return the user's permanent address 2."""
        return instance.user.profile.address2
    address2.short_description = "Address2 permanent"

    def city(self, instance):
        """Return the user's city."""
        return instance.user.profile.city
    city.short_description = "City permanent"

    def state(self, instance):
        """Return the user's state."""
        return instance.user.profile.state
    state.short_description = "State permanent"

    def postal_code(self, instance):
        """Return the user's postal code."""
        return instance.user.profile.postal_code
    postal_code.short_description = "Postal code permanent"

    def address1_current(self, instance):
        """Return the user's current address."""
        return instance.user.profile.address1_current

    def address2_current(self, instance):
        """Return the user's current address 2."""
        return instance.user.profile.address2_current

    def city_current(self, instance):
        """Return the user's current city."""
        return instance.user.profile.city_current

    def state_current(self, instance):
        """Return the user's current state."""
        return instance.user.profile.state_current

    def postal_code_current(self, instance):
        """Return the user's current postal code."""
        return instance.user.profile.postal_code_current

    def date_of_birth(self, instance):
        """Return the user's date of birth."""
        return instance.user.profile.date_of_birth

    def gender(self, instance):
        """Return the user's gender."""
        return instance.user.profile.gender

    def disability(self, instance):
        """Return the user's disability status."""
        return instance.user.profile.disability

    def disability_specify(self, instance):
        """Return the user's disability specifics."""
        return instance.user.profile.disability_specify

    def us_citizen(self, instance):
        """Return the user's US citizen status."""
        return instance.user.profile.us_citizen

    def employment(self, instance):
        """Return the user's employment status."""
        return instance.user.profile.employment

    def military(self, instance):
        """Return the user's military status."""
        return instance.user.profile.military

    def race(self, instance):
        """Return the user's race/s."""
        return '/'.join([raza.name for raza in instance.user.profile.race.all()])

    def tribe(self, instance):
        """Return the user's tribe."""
        return instance.user.profile.tribe

    def email(self, instance):
        """Return the user's primary email."""
        return '<a href="mailto:{0}">{1}</a>'.format(
            instance.user.email, instance.user.email,
        )
    email.allow_tags = True
    email.short_description = 'Email'

    def email_auxiliary(self, instance):
        """Return the user's secondary email."""
        return get_email_auxiliary(instance.user)

    def registration_type(self, instance):
        """Return the user's registration type."""
        try:
            reg_type = '<a href="{0}">{1}</a>'.format(
                reverse(
                    'admin:registration_{0}_change'.format(
                        instance.user.profile.registration_type.lower(),
                    ),
                    args=(instance.user.profile.get_registration().id,),
                ),
                instance.user.profile.registration_type,
            )
        except Exception:
            return None
        return reg_type
    registration_type.allow_tags = True
    registration_type.short_description = 'Reg Type (view/edit)'

    def wsgc_affiliate(self, instance):
        """Return the user's WSGC affiliate organization."""
        try:
            wsgc_affiliate = instance.user.profile.get_registration().wsgc_affiliate
        except Exception:
            wsgc_affiliate = None
        try:
            if wsgc_affiliate.name == 'Other':
                wsgc_affiliate = instance.user.profile.get_registration().wsgc_affiliate_other
        except Exception:
            pass
        return wsgc_affiliate
    wsgc_affiliate.short_description = "Institution Name"

    def mugshot_file(self, instance):
        """Return the user's mugshot file."""
        try:
            return admin_display_file(instance.user.user_files, 'mugshot')
        except Exception:
            return '<i class="fa fa-times-circle red" aria-hidden="true"></i>'
    mugshot_file.allow_tags = True
    mugshot_file.short_description = "Photo"

    def biography_file(self, instance):
        """Return the user's biography file."""
        try:
            return admin_display_file(instance.user.user_files, 'biography')
        except Exception:
            return '<i class="fa fa-times-circle red" aria-hidden="true"></i>'
    biography_file.allow_tags = True
    biography_file.short_description = "Bio"

    def media_release_file(self, instance):
        """Return the user's media release file."""
        try:
            return admin_display_file(instance.user.user_files, 'media_release')
        except Exception:
            return '<i class="fa fa-times-circle red" aria-hidden="true"></i>'
    media_release_file.allow_tags = True
    media_release_file.short_description = "Media"

    def irs_w9_file(self, instance):
        """Return the user's IRS W9 file."""
        try:
            return admin_display_file(instance.user.user_files, 'irs_w9')
        except Exception:
            return '<i class="fa fa-times-circle red" aria-hidden="true"></i>'
    irs_w9_file.allow_tags = True
    irs_w9_file.short_description = "W9"

    def award_acceptance_file(self, instance):
        """Return the user's Award Acceptance file."""
        return admin_display_file(instance, 'award_acceptance')
    award_acceptance_file.allow_tags = True
    award_acceptance_file.short_description = "Award Accpt"

    def interim_report_file(self, instance):
        """Return the user's Interim Report file."""
        return admin_display_file(instance, 'interim_report')
    interim_report_file.allow_tags = True
    interim_report_file.short_description = "Interim Rpt"

    def final_report_file(self, instance):
        """Return the user's Final Report file."""
        return admin_display_file(instance, 'final_report')
    final_report_file.allow_tags = True
    final_report_file.short_description = "Final Rpt"

    def other_file_file(self, instance):
        """Return the user's other file 1."""
        return admin_display_file(instance, 'other_file')
    other_file_file.allow_tags = True
    other_file_file.short_description = "Other1"

    def other_file2_file(self, instance):
        """Return the user's other file 2."""
        return admin_display_file(instance, 'other_file2')
    other_file2_file.allow_tags = True
    other_file2_file.short_description = "Other2"

    def other_file3_file(self, instance):
        """Return the user's other file 3."""
        return admin_display_file(instance, 'other_file3')
    other_file3_file.allow_tags = True
    other_file3_file.short_description = "Other3"

    def save_model(self, request, instance, form, change):
        """Override the save_model method to set updated_by value."""
        instance.updated_by = request.user
        instance.save()


class GenericChoiceAdmin(admin.ModelAdmin):
    """Generic Choice admin."""

    list_display = ('name', 'value', 'ranking', 'active')


class ProfileAdmin(admin.ModelAdmin):
    """User profile admin."""

    list_display = ['last_name', 'first_name', 'email', 'username', 'id']
    ordering = ['user__last_name', 'user__first_name', 'id']
    search_fields = (
        'user__last_name',
        'user__first_name',
        'user__email',
        'user__username',
        'user__id',
    )
    date_hierarchy = 'date_created'
    list_per_page = 500
    raw_id_fields = ('user', 'updated_by')

    def last_name(self, instance):
        """Return the user's last name."""
        return instance.user.last_name

    def first_name(self, instance):
        """Return the user's first name."""
        return instance.user.first_name

    def email(self, instance):
        """Return the user's email."""
        return instance.user.email

    def username(self, instance):
        """Return the user's username."""
        return instance.user.username

    def save_model(self, request, instance, form, change):
        """Override the save_model method to set updated_by value."""
        instance.updated_by = request.user
        instance.save()


# override django admin user display
class UserProfileInline(admin.StackedInline):
    """User profile inline admin class."""

    model = UserProfile
    can_delete = False
    # we need this because UserProfile has two FK to auth.User model
    fk_name = 'user'


class UserProfileAdmin(UserAdmin):
    """User profile admin class."""

    inlines = (UserProfileInline,)


admin.site.register(GenericChoice, GenericChoiceAdmin)
admin.site.unregister(User)
admin.site.register(User, UserProfileAdmin)
admin.site.register(UserProfile, ProfileAdmin)
