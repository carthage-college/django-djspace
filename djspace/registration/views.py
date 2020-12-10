# -*- coding: utf-8 -*-

import django
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import Http404
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from djspace.registration.forms import *
from djspace.registration.models import *
from djtools.utils.convert import str_to_class


@login_required
def form(request, reg_type):
    """Generic form method that handles all registration types."""
    user = request.user

    # check if someone is up to something
    if user.profile.registration_type != reg_type:
        return HttpResponseRedirect(reverse('dashboard_home'))
    try:
        mod = django.apps.apps.get_model(
            app_label='registration', model_name=reg_type,
        )
        reg = mod.objects.get(user=user)
    except Exception:
        reg = None
    try:
        reg_form = str_to_class(
            'djspace.registration.forms', '{0}Form'.format(reg_type),
        )(instance=reg, use_required_attribute=False)
    except Exception:
        raise Http404

    if request.method == 'POST':
        try:
            reg_form = str_to_class(
                'djspace.registration.forms', '{0}Form'.format(reg_type),
            )(instance=reg, data=request.POST, use_required_attribute=False)
        except Exception:
            raise Http404
        if reg_form.is_valid():
            reggie = reg_form.save(commit=False)
            reggie.user = user
            reggie.updated_by = user
            reggie.save()
            return HttpResponseRedirect(reverse('registration_success'))

    return render(
        request, 'registration/form.html', {'form': reg_form, 'reg_type': reg_type},
    )


@login_required
def user_files(request):
    """User files form."""
    user_files_form = UserFilesForm(use_required_attribute=False)

    return render(
        request, 'registration/user_files.html', {'form': user_files_form},
    )


@staff_member_required
def registration_print(request, uid):
    """Registration print view."""
    user = get_object_or_404(User, pk=uid)
    return render(
        request, 'application/email/base.html', {'data': {'user': user}},
    )
