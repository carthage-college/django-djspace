from django.conf import settings
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response

from djspace.core.models import UserProfile
from djspace.dashboard.forms import UserProfileForm

from djtools.utils.mail import send_mail

#@login_required
def home(request):
    profile = UserProfile.objects.get(user=request.user)
    form = UserProfileForm(instance=profile)
    return render_to_response(
        "dashboard/home.html",
        {"form": form,},
        context_instance=RequestContext(request)
    )
