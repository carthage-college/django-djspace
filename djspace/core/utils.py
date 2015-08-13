from django.conf import settings
from allauth.account.models import EmailAddress

from djtools.fields import NOW
from djtools.utils.mail import send_mail

from datetime import datetime

def get_profile_status(user):
    """
    simple function that compares the user's profile updated datetime
    against the grant cycle start date, which is comprised of the
    current year and the settings value for the month and the first
    day of the month.
    """
    grant_cycle_start_date = datetime(
        NOW.year, settings.GRANT_CYCLE_START_MES, 1
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
        filter(primary=False).order_by("-id")
    if e:
        # we really only need the first one
        return e[0]
    else:
        return None
