from django.conf import settings
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

from djspace.registration.forms import *
from djspace.core.models import UserProfile
from djspace.dashboard.forms import UserProfileForm

from djtools.utils.mail import send_mail

@login_required
def home(request):
    """
    User dashboard home
    """

@login_required
def profile_form(request):
    """
    Form method that handles user profile data.
    """
    message = None
    user = request.user
    profile = UserProfile.objects.get(user=user)
    reg_type = profile.registration_type
    try:
        reg = eval(reg_type).objects.get(user=user)
    except:
        reg = None

    reg_form = eval(reg_type+"Form")(instance=reg)
    if request.method == 'POST':
        form = UserProfileForm(instance=profile, data=request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.user = user
            data.save()
            message = "Success"
    else:
        form = UserProfileForm(instance=profile)
    return render_to_response(
        "dashboard/profile_form.html", {
            "form":form,"reg_form":reg_form,
            "reg_type":reg_type,"message":message
        }, context_instance=RequestContext(request)
    )
