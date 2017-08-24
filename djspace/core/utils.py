from django.conf import settings
from django.forms.models import model_to_dict

from djtools.fields import NOW
from djtools.utils.mail import send_mail
from djtools.utils.cypher import AESCipher

from datetime import datetime
import os

PROFESSIONAL_PROGRAMS = [
    "aerospaceoutreach",
    "highereducationinitiatives",
    "industryinternship",
    "nasacompetition",
    "researchinfrastructure",
    "specialinitiatives",
]

# rocket launch required files by competition. this will do until
# we change the data model to have a separate table for their files
MRL_REQUIRED_FILES = [
    "preliminary_design_report","flight_readiness_report",
    "education_outreach","post_flight_performance_report",
    "proceeding_paper"
]
FNL_REQUIRED_FILES = [
    "budget","flight_demo","preliminary_design_report",
    "final_motor_selection","lodging_list","critical_design_report",
    "oral_presentation","post_flight_performance_report"
]
CRL_REQUIRED_FILES = [
    "budget","flight_demo","interim_progress_report",
    "final_design_report","education_outreach","oral_presentation",
    "post_flight_performance_report","proceeding_paper"
]


def get_start_date():

    year = NOW.year
    if NOW.month < settings.GRANT_CYCLE_START_MES:
        year = NOW.year - 1
    start_date = datetime(
        year, settings.GRANT_CYCLE_START_MES, 1
    )

    return start_date


def upload_to_path(field_name, instance, filename):
    """
    Generates the path as a string for file field.
    """

    cipher = AESCipher(bs=16)
    cid = cipher.encrypt(str(instance.user.id))
    ext = filename.split('.')[-1]
    filename = u'{}_{}.{}'.format(instance.get_file_name(),field_name, ext)
    path = "{}/{}/{}/".format(
        instance.get_file_path(), instance.get_slug(), cid
    )
    return os.path.join(path, filename)


def files_status(user):

    status = True
    start_date = get_start_date()

    # fetch all user application submissions
    apps = user.profile.applications.all()
    # First Nations Competition exception
    fnl = False
    for app in apps:
        if app.get_content_type().model == "firstnationsrocketcompetition":
            fnl = True

    # ignore FNL altogether for user files:
    # bio, mugshot, media release, w9
    if not fnl:
        files = user.user_files
        # check for user profile files
        try:
            data=model_to_dict(files)
        except:
            # UserFiles() instance does not exist
            return False
        for k,v in data.items():
            if not v:
                return False
            # have to be renewed every year
            if k != 'id' and not files.status(k):
                return False

    # check for application files
    for app in apps:

        data=model_to_dict(app)

        # all programs except FNL
        if not app.award_acceptance and not fnl:
            return False

        # program specific
        m = app.get_content_type().model
        # professional programs
        if m in PROFESSIONAL_PROGRAMS:
            if not data['close_out_finance_document']:
                return False

        # rocket launch team files
        # (not very elegant but waiting on new data model)
        if m == "rocketlaunchteam":
            if app.competition == "Collegiate Rocket Competition":
                for field in CRL_REQUIRED_FILES:
                    if not getattr(app,field):
                        return False
            elif app.competition == "Midwest High Powered Rocket Competition":
                for field in MRL_REQUIRED_FILES:
                    if not getattr(app,field):
                        return False
            else:
                for field in FNL_REQUIRED_FILES:
                    if not getattr(app,field):
                        return False

    return status


def profile_status(user):
    """
    simple function that compares the user's profile updated datetime
    against the grant cycle start date, which is comprised of the
    current year and the settings value for the month and the first
    day of the month.
    """
    status = False
    if user.profile.date_updated > get_start_date():
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

def get_term(date):
    term = "SP"
    if date.month >= settings.GRANT_CYCLE_START_MES:
        term = "FA"
    return term

def get_email_auxiliary(user):
    from allauth.account.models import EmailAddress
    e = EmailAddress.objects.filter(user=user).\
        filter(primary=False).order_by("-id")[:1]
    if len(e) > 0:
        return e[0].email
    else:
        return None

def admin_display_file(instance, field):
    icon = '<i class="fa fa-times-circle red" aria-hidden="true"></i>'
    attr = getattr(instance, field)
    if attr:
        icon = '''<a href="{}" target="_blank">
          <i class="fa fa-check green" aria-hidden="true"></i>
        </a>'''.format(attr.url)
    return icon

