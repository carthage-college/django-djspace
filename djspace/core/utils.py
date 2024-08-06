# -*- coding: utf-8 -*-

import os
import secrets
from datetime import datetime

from allauth.account.models import EmailAddress
from django.conf import settings
from django.forms.models import model_to_dict
from django.utils.safestring import mark_safe
from djtools.utils.mail import send_mail


PROFESSIONAL_PROGRAMS = [
    'aerospaceoutreach',
    'earlystageinvestigator',
    'highereducationinitiatives',
    'industryinternship',
    'nasacompetition',
    'researchinfrastructure',
    'specialinitiatives',
]
# rocket launch required files by competition. this will do until
# we change the data model to have a separate table for their files
MRL_REQUIRED_FILES = [
    'preliminary_design_report',
    'flight_readiness_report',
    'education_outreach',
    'post_flight_performance_report',
    'proceeding_paper',
]
FNL_REQUIRED_FILES = [
    'budget',
    'flight_demo',
    'preliminary_design_report',
    'final_motor_selection',
    'lodging_list',
    'critical_design_report',
    'oral_presentation',
    'post_flight_performance_report',
]
CRL_REQUIRED_FILES = [
    'budget',
    'flight_demo',
    'interim_progress_report',
    'final_design_report',
    'education_outreach',
    'oral_presentation',
    'post_flight_performance_report',
    'proceeding_paper',
]


def get_start_date():
    """Obtain the start date for the current grant cycle."""
    now = datetime.now()
    year = now.year
    if now.month < settings.GRANT_CYCLE_START_MES:
        year = now.year - 1
    return datetime(year, settings.GRANT_CYCLE_START_MES, 1)


def upload_to_path(field_name, instance, filename):
    """Generates the path as a string for file field."""
    cid = secrets.token_urlsafe(32)
    ext = filename.split('.')[-1]
    if field_name == 'Program_Photo':
        field_name = '{0}_{1}'.format(
            field_name, instance.content_object.get_photo_suffix(),
        )
    filename = '{0}_{1}.{2}'.format(instance.get_file_name(), field_name, ext)
    path = '{0}/{1}/{2}/'.format(
        instance.get_file_path(), instance.get_slug(), cid,
    )
    return os.path.join(path, filename)


def files_status(user):
    """Determine if the user file is valid for the current grant cycle."""
    status = True
    # fetch all user application submissions
    apps = user.profile.applications.all()
    # First Nations Competition exception
    fnl = False
    for ap in apps:
        if ap.get_content_type().model == 'firstnationsrocketcompetition':
            fnl = True

    # ignore FNL altogether for user files:
    # bio, mugshot, media release, w9
    if not fnl:
        try:
            files = user.user_files
            files_dict = model_to_dict(files)
        except Exception:
            # UserFiles() instance does not exist
            return False
        for key, valu in files_dict.items():
            if key != 'id':
                if not valu:
                    return False
                # have to be renewed every year
                if not files.status(key):
                    return False

    # check for application files
    for app in apps:
        if app.status:
            app_dict = model_to_dict(app)

            # all programs except FNL
            if not app.award_acceptance and not fnl:
                return False

            # program specific
            mod = app.get_content_type().model
            # professional programs
            if mod in PROFESSIONAL_PROGRAMS:
                if not app_dict['close_out_finance_document']:
                    return False

            # rocket launch team files
            # (not very elegant but waiting on new data model)
            if mod == 'rocketlaunchteam':
                if app.competition == 'Collegiate Rocket Competition':
                    for cfield in CRL_REQUIRED_FILES:
                        if not getattr(app, cfield):
                            return False
                elif app.competition == 'Midwest High Powered Rocket Competition':
                    for mfield in MRL_REQUIRED_FILES:
                        if not getattr(app, mfield):
                            return False
                else:
                    for ffield in FNL_REQUIRED_FILES:
                        if not getattr(app, ffield):
                            return False

    return status


def profile_status(user):
    """
    Determine the status of the user's registration profile.

    Compares the user's profile updated datetime against the grant cycle
    start date, which is comprised of the current year and the settings
    value for the month and the first day of the month.
    """
    status = False
    mr = user.profile.media_release
    if user.profile.date_updated >= get_start_date():
        if mr in {'I agree', 'I am a minor'}:
            status = True
    return status


def registration_notify(request, action, user):
    """Send an email when a new registration comes in."""
    subject = "[WSGC Profile Registration: {0}D] {1}, {2}".format(
        action.upper(), user.last_name, user.first_name,
    )
    if settings.DEBUG:
        to_list = [settings.ADMINS[0][1]]
    else:
        to_list = [settings.WSGC_APPLICATIONS]
    template = 'account/registration_alert_email.html'
    context = {
        'user': user,
        'action': action,
        'server_url': settings.SERVER_URL,
        'media_url': settings.MEDIA_URL,
    }
    frum = user.email
    send_mail(
        request,
        to_list,
        subject,
        frum,
        template,
        context,
        reply_to=[frum,],
        bcc=[settings.ADMINS[0][1]],
    )


def get_term(date):
    """Obtain the current term for the grant cycle."""
    term = 'SP'
    if date.month >= settings.GRANT_CYCLE_START_MES:
        term = 'FA'
    return term


def get_email_auxiliary(user):
    """Fetch the secondary email address for the user."""
    return EmailAddress.objects.filter(user=user).filter(
        primary=False,
    ).order_by('-id').first()


def admin_display_file(instance, field, team=False):
    """Display the proper icon on the admin dashboard for the file."""
    status = False
    if team:
        attr = getattr(instance.team, field)
    else:
        attr = getattr(instance, field)
    # user profile files expire each grant cycle
    if attr and field in {'mugshot', 'biography', 'irs_w9'}:
        status = instance.user.user_files.status(field)
        if status:
            icon = mark_safe(
                """<a href="{0}" target="_blank">
                <i class="fa fa-check green" aria-hidden="true"></i></a>
                """.format(attr.url),
            )
        else:
            icon = mark_safe('<i class="fa fa-times-circle red" aria-hidden="true"></i>')
    elif team:
        if attr:
            icon = mark_safe(
                """<a href="{0}" target="_blank">
                <i class="fa fa-check green" aria-hidden="true"></i></a>
                """.format(attr.url),
            )
        else:
            icon = mark_safe('<i class="fa fa-times-circle red" aria-hidden="true"></i>')
    elif attr:
        icon = mark_safe(
            """<a href="{0}" target="_blank">
            <i class="fa fa-check green" aria-hidden="true"></i></a>
            """.format(attr.url),
        )
    else:
        icon = mark_safe('<i class="fa fa-times-circle red" aria-hidden="true"></i>')
    return icon
