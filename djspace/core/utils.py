from django.conf import settings
from django.forms.models import model_to_dict
from allauth.account.models import EmailAddress

from djtools.fields import NOW
from djtools.utils.mail import send_mail

from datetime import datetime
import os


def upload_to_path(self, filename):
    """
    Generates the path as a string for file field.
    """

    ext = filename.split('.')[-1]
    # set filename as random string
    filename = '{}.{}'.format(self.get_file_name(), ext)
    path = "{}/{}/{}/".format(
        self.get_file_path(), self.get_slug(), self.user.id
    )
    return os.path.join(path, filename)


def files_status(user):

    status = True

    # check for user profile files
    data=model_to_dict(user.user_files)
    for k,v in data.items():
        if not v:
            return False

    # check for application files
    for app in user.profile.applications.all():

        data=model_to_dict(app)

        # all programs
        if not app.award_acceptance:
            return False

        # program specific
        m = app.get_content_type().model
        # professional programs
        if m in PROFESSIONAL_PROGRAMS:
            if not data["interim_report"] or not data["final_report"]:
                return False

        # rocket launch team files
        if m == "rocketlaunchteam":
            if app.competition == "Collegiate Rocket Competition":
                pass
            elif app.competition == "Midwest High Powered Rocket Competition":
                pass
            else:
                pass

    return status


def profile_status(user):
    """
    simple function that compares the user's profile updated datetime
    against the grant cycle start date, which is comprised of the
    current year and the settings value for the month and the first
    day of the month.
    """
    year = NOW.year
    if NOW.month < settings.GRANT_CYCLE_START_MES:
        year = NOW.year - 1
    grant_cycle_start_date = datetime(
        year, settings.GRANT_CYCLE_START_MES, 1
    )
    status = False
    if user.profile.date_updated > grant_cycle_start_date:
        status = True
    return status

def registration_notify(request, action, user):
    subject = u"[WSGC Profile Registration: {}D] {}, {}".format(
        action.upper(), user.last_name, user.first_name
    )
    if settings.DEBUG:
        TO_LIST = [settings.ADMINS[0][1],]
    else:
        TO_LIST = [settings.WSGC_APPLICATIONS,]
    template = "account/registration_alert_email.html"
    send_mail(
        request, TO_LIST, subject, user.email,
        template, {"user":user,"action":action}, settings.MANAGERS
    )

def get_email_auxiliary(user):
    e = EmailAddress.objects.filter(user=user).\
        filter(primary=False).order_by("-id")[:1]
    if len(e) > 0:
        return e[0].email
    else:
        return None

