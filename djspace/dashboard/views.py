from django.conf import settings
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

from djspace.core.models import UserProfile
from djspace.dashboard.forms import UserProfileForm

from djtools.utils.mail import send_mail

@login_required
def home(request):
    message = None
    profile = UserProfile.objects.get(user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(instance=profile, data = request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.user = request.user
            data.save()
            message = "Success"
    else:
        form = UserProfileForm(instance=profile)
    return render_to_response(
        "dashboard/home.html",
        {"form": form,"message":message},
        context_instance=RequestContext(request)
    )
