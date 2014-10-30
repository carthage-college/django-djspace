from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required

from djspace.registration.forms import *

@login_required
def form(request, reg_type):
    """
    Generic form method that handles all registration types.
    """
    user = request.user
    # check if someone is up to something
    if user.profile.registration_type != reg_type:
        return HttpResponseRedirect(reverse('dashboard_home'))
    try:
        reg = eval(reg_type).objects.get(user=user)
    except:
        reg = None
    try:
        form = eval(reg_type+"Form")(instance=reg)
    except:
        raise Http404
    if request.method == 'POST':
        try:
            form = eval(reg_type+"Form")(instance=reg, data=request.POST)
        except:
            raise Http404
        if form.is_valid():
            data = form.save(commit=False)
            data.user = user
            data.updated_by = user
            data.save()
            return HttpResponseRedirect(reverse('registration_success'))

    return render_to_response(
        "registration/form.html",
        {"form": form,"reg_type":reg_type},
        context_instance=RequestContext(request)
    )

