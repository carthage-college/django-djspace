from django.db.models import Q
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.forms.models import model_to_dict
from django.utils.safestring import mark_safe
from django.shortcuts import render_to_response
from django.template import RequestContext, loader
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required

from djspace.registration.forms import *
from djspace.core.utils import get_profile_status
from djspace.dashboard.forms import UserForm, UserProfileForm

from djtools.utils.convert import str_to_class

import json


@login_required
def home(request):
    """
    User dashboard home
    """

    user = request.user
    try:
        mod = str_to_class(
            "djspace.registration.models",
            user.profile.registration_type
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

    status = get_profile_status(user)
    return render_to_response(
        "dashboard/home.html", {"reg":reg,"status":status},
        context_instance=RequestContext(request)
    )


@csrf_exempt
def get_users(request):
    """
    AJAX GET for retrieving users via auto-complete
    """

    if request.is_ajax():
        q = request.GET.get('term', '')

        users = User.objects.filter(
            Q( first_name__icontains = q ) |
            Q( last_name__icontains = q ) |
            Q( username__icontains = q ) ).order_by( 'last_name' )

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
def registration_type(request):
    """
    AJAX post for retrieving registration forms based on type
    """
    if request.method == 'POST':
        reg_type = request.POST.get("registration_type")
        try:
            mod = str_to_class(
                "djspace.registration.models", reg_type
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
        mod = str_to_class(
            "djspace.registration.models", reg_type
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
    return render_to_response(
        "dashboard/profile_form.html", {
            "pro_form":pro_form,"reg_form":reg_form,"usr_form":usr_form,
            "reg_type":reg_type,"message":message
        }, context_instance=RequestContext(request)
    )
