from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
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
            'djspace.registration.forms', (reg_type+'Form')
        )(instance=reg, use_required_attribute=False)
    except:
        raise Http404

    if request.method == 'POST':
        try:
            form = str_to_class(
                'djspace.registration.forms', (reg_type+'Form')
            )(instance=reg, data=request.POST, use_required_attribute=False)
        except:
            raise Http404
        if form.is_valid():
            data = form.save(commit=False)
            data.user = user
            data.updated_by = user
            data.save()
            return HttpResponseRedirect(reverse('registration_success'))

    return render(
        request, 'registration/form.html', {'form': form,'reg_type':reg_type}
    )

@login_required
def user_files(request):

    form = UserFilesForm(use_required_attribute=False)

    return render(
        request, 'registration/user_files.html', {'form': form,}
    )


@staff_member_required
def registration_print(request, uid):

    user = get_object_or_404(User, pk=uid)
    user = user
    return render(
        request, 'application/email/base.html', {'data': {'user':user,},}
    )
