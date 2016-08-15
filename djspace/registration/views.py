from django.template import RequestContext
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required

from djspace.registration.forms import *
from djspace.registration.models import *
from djtools.utils.convert import str_to_class

import django


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
        mod = django.apps.apps.get_model(
            app_label='registration', model_name=reg_type
        )
        reg = mod.objects.get(user=user)
    except:
        reg = None
    try:
        form = str_to_class(
            "djspace.registration.forms", (reg_type+"Form")
        )(instance=reg)
    except:
        raise Http404

    if request.method == 'POST':
        try:
            form = str_to_class(
                "djspace.registration.forms", (reg_type+"Form")
            )(instance=reg, data=request.POST)
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

@login_required
def user_files(request):

    form = UserFilesForm()

    return render_to_response(
        "registration/user_files.html",
        {"form": form,},
        context_instance=RequestContext(request)
    )


@staff_member_required
def registration_print(request, uid):

    user = get_object_or_404(User, pk=uid)
    user = user
    return render_to_response(
        "application/email/base.html",
        {'data': {'user':user,},},
        context_instance=RequestContext(request)
    )
