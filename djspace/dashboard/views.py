from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.forms.models import model_to_dict
from django.utils.safestring import mark_safe
from django.shortcuts import render
from django.template import RequestContext, loader
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse, HttpResponseRedirect, Http404


from djspace.application.forms import *
from djspace.registration.forms import *
from djspace.core.utils import get_start_date
from djspace.core.utils import profile_status, files_status
from djspace.core.utils import PROFESSIONAL_PROGRAMS
from djspace.application.models import ROCKET_COMPETITIONS_EXCLUDE
from djspace.dashboard.forms import UserForm, UserProfileForm
from djspace.core.forms import UserFilesForm
from djspace.core.models import UserFiles

from djtools.utils.convert import str_to_class

import json
import django

UPLOAD_FORMS = {
  "highereducationinitiatives": HigherEducationInitiativesUploadsForm,
  "researchinfrastructure": ResearchInfrastructureUploadsForm,
  "aerospaceoutreach": AerospaceOutreachUploadsForm,
  "specialinitiatives": SpecialInitiativesUploadsForm,
  "undergraduatescholarship": UndergraduateScholarshipUploadsForm,
  "stembridgescholarship": StemBridgeScholarshipUploadsForm,
  "undergraduateresearch": UndergraduateResearchUploadsForm,
  "graduatefellowship": GraduateFellowshipUploadsForm,
  "clarkgraduatefellowship": ClarkGraduateFellowshipUploadsForm,
  "highaltitudeballoonpayload": HighAltitudeBalloonPayloadUploadsForm,
  "highaltitudeballoonlaunch": HighAltitudeBalloonLaunchUploadsForm,
  "rocketlaunchteam": RocketLaunchTeamUploadsForm,
  "firstnationsrocketcompetition": FirstNationsRocketCompetitionUploadsForm,
  "midwesthighpoweredrocketcompetition": MidwestHighPoweredRocketCompetitionUploadsForm,
  "collegiaterocketcompetition": CollegiateRocketCompetitionUploadsForm,
  "nasacompetition": NasaCompetitionUploadsForm,
  "industryinternship": IndustryInternshipUploadsForm,
  'professionalprogramstudent': ProfessionalProgramStudentUploadsForm
}


@login_required
def home(request):
    """
    User dashboard home
    """

    user = request.user
    try:
        files = UserFiles.objects.get(user=user)
    except:
        files = None

    user_files = UserFilesForm(instance=files)
    try:
        mod = django.apps.apps.get_model(
            app_label='registration', model_name=user.profile.registration_type
        )
        reg = mod.objects.get(user=user)
    except:
        reg = None

    # if the user does not have any applications, the gm2m
    # field will throw an error
    try:
        apps = user.profile.applications
    except:
        apps = None

    # all applications
    applications = []
    # only approved, which we can eventually use to display list
    approved = []
    # we need the content type ID for rocket launch team only
    # since team leaders can upload file for that model
    team = {}
    start_date = get_start_date()
    for a in apps.all():
        if a.multi_year or a.date_created >= start_date:
            applications.append(a)
            if a.status:
                approved.append(a)
            if "rocketcompetition" in a.get_content_type().model:
                # in case the team has no leader, somehow.
                try:
                    if a.team.leader.id == user.id:
                        team['ct'] = a.team.get_content_type().id
                        team['id'] = a.team.id
                except:
                    pass

    # check if the user has upload all of her user files
    if approved:
        user_files_status = files_status(user)
        if not user_files_status:
            messages.add_message(
                request, messages.ERROR,
                '''
                You have not uploaded required files. Please do so below.
                ''',
                extra_tags='danger'
            )

    status = profile_status(user)

    return render(
        request, 'dashboard/home.html', {
            'user_files':user_files,
            'reg':reg,'status':status,'approved':approved,
            'mugshot_status':files.status('mugshot'),
            'biography_status':files.status('biography'),
            'irs_w9_status':files.status('irs_w9'),
            'media_release_status':files.status('media_release'),
            'team':team,'applications':applications,
            'professional_programs':PROFESSIONAL_PROGRAMS,
            'rocket_competitions':ROCKET_COMPETITIONS_EXCLUDE
        }
    )


@csrf_exempt
@login_required
def get_users(request):
    """
    AJAX GET for retrieving users via auto-complete
    """

    if request.is_ajax():
        q = request.GET.get('term', '')

        users = User.objects.filter(
            Q( first_name__icontains = q ) |
            Q( last_name__icontains = q ) ).order_by( 'last_name' )

        #users = User.objects.filter(last_name__icontains = q )[:20]
        results = []
        for u in users:
            user_json = {}
            name = u"{}, {}".format(u.last_name, u.first_name)
            user_json['id'] = u.id
            user_json['label'] = name
            user_json['value'] = name
            results.append(user_json)

    return HttpResponse(
        json.dumps(results),
        content_type="application/json; charset=utf-8"
    )


@csrf_exempt
@login_required
def registration_type(request):
    """
    AJAX post for retrieving registration forms based on type
    """
    if request.method == 'POST':
        reg_type = request.POST.get("registration_type")
        try:
            mod = django.apps.apps.get_model(
                app_label='registration', model_name=reg_type
            )
            reg = mod.objects.get(user=request.user)
        except:
            reg = None
        try:
            reg_form = str_to_class(
                "djspace.registration.forms", (reg_type+"Form")
            )(instance=reg, prefix="reg")
        except:
            raise Http404
        reggie = None
        if reg:
            reggie = model_to_dict(reg)
        t = loader.get_template("dashboard/registration_form.inc.html")
        c = RequestContext(
            request, {"reg_form":reg_form,'reg_type':reg_type}
        )
        data = {'form':t.render(c),'reg':reggie,'reg_type':reg_type}
        response = HttpResponse(
            json.dumps(data),
            content_type="application/json; charset=utf-8"
        )
        return response
    else:
        raise Http404


@login_required
def profile_form(request):
    """
    Form method that handles user profile data.
    """
    message = None
    user = request.user
    profile = user.profile
    reg_type = profile.registration_type
    reg_data = None
    # user may have changed registration type
    if request.method == 'POST' and reg_type != request.POST.get("pro-registration_type"):
        reg_type = request.POST.get("pro-registration_type")
    try:
        mod = django.apps.apps.get_model(
            app_label='registration', model_name=reg_type
        )
        reg = mod.objects.get(user=user)
    except:
        reg = None
    if request.method == 'POST':

        reg_form = str_to_class(
            "djspace.registration.forms", (reg_type+"Form")
        )(instance=reg, prefix="reg", data=request.POST)

        pro_form = UserProfileForm(
            instance=profile, data=request.POST, prefix="pro"
        )
        usr_form = UserForm(prefix="usr", data=request.POST)
        if pro_form.is_valid() and reg_form.is_valid() and usr_form.is_valid():
            usr = usr_form.cleaned_data
            user.first_name = usr["first_name"]
            user.last_name = usr["last_name"]
            user.save()
            pro = pro_form.save(commit=False)
            pro.salutation = usr["salutation"]
            pro.second_name = usr["second_name"]
            pro.updated_by = user
            pro.user = user
            pro.save()
            reg = reg_form.save(commit=False)
            reg.user = user
            reg.updated_by = user
            reg.save()
            message = "Success"
    else:
        usr_form = UserForm(initial={
            'salutation':profile.salutation,'first_name':user.first_name,
            'second_name':profile.second_name,'last_name':user.last_name
        }, prefix="usr")
        reg_form = str_to_class(
            "djspace.registration.forms", (reg_type+"Form")
        )(instance=reg, prefix="reg")
        pro_form = UserProfileForm(instance=profile, prefix="pro")
    return render(
        request, "dashboard/profile_form.html", {
            "pro_form":pro_form,"reg_form":reg_form,"usr_form":usr_form,
            "reg_type":reg_type,"message":message
        }
    )


@csrf_exempt
@login_required
def set_val(request):
    """
    AJAX POST for setting arbitrary values to an object
    """

    user = request.user
    msg = "fail"
    obj = None
    if request.method != "POST":
        msg = "POST required"
    else:

        cid = request.POST.get("cid")
        oid = request.POST.get("oid")
        field = request.POST.get("field")
        value = request.POST.get("value")

        try:
            ct = ContentType.objects.get(pk=int(cid))
            mod = ct.model_class()
            obj = mod.objects.get(pk=int(oid))
        except:
            msg = """
                Could not retrieve ContentType ({}) or object ({})
            """.format(cid, oid)

        if obj:
            # team leaders can upload files for rocket launch teams
            leader = False
            if ct.model == "rocketlaunchteam":
                if obj.leader.id == user.id:
                    leader = True
            # is someone being naughty?
            if obj.user != user and not leader:
                msg =  "Something is rotten in Denmark"
            else:
                setattr(obj, field, value)
                msg = "success"
            obj.save()

    return HttpResponse(
        msg, content_type="text/plain; charset=utf-8"
    )

