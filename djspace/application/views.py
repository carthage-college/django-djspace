# -*- coding: utf-8 -*-
from django.conf import settings
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404

from djspace.application.forms import *
from djspace.registration.models import *
from djspace.core.utils import get_profile_status

from djtools.utils.mail import send_mail

@login_required
def form(request, application_type, aid=None):

    # verify that the user has completed registration
    reg_type = request.user.profile.registration_type
    try:
        reg = eval(reg_type).objects.get(user=request.user)
    except:
        # redirect to dashboard
        return HttpResponseRedirect(reverse('dashboard_home'))

    # verify that the user has an up to date registration
    if not get_profile_status(request.user):
        # redirect to dashboard
        return HttpResponseRedirect(reverse('dashboard_home'))

    if settings.DEBUG:
        TO_LIST = [settings.ADMINS[0][1],]
    else:
        TO_LIST = [settings.WSGC_APPLICATIONS,]
    BCC = settings.MANAGERS
    user = request.user
    slug_list = application_type.split("-")
    app_name = slug_list.pop(0).capitalize()
    for n in slug_list:
        app_name += " %s" % n.capitalize()
    app_type = "".join(app_name.split(" "))

    app = None
    if aid:
        if request.user.is_superuser:
            app = eval(app_type).objects.get(pk=aid)
        else:
            # prevent users from managing apps that are not theirs
            try:
                app = eval(app_type).objects.get(pk=aid, user=user)
            except:
                app = None
    try:
        form = eval(app_type+"Form")(instance=app)
    except:
        # app_type does not match an existing form
        raise Http404

    if request.method == 'POST':
        try:
            form = eval(app_type+"Form")(
                instance=app, data=request.POST, files=request.FILES
            )
        except:
            # app_type does not match an existing form
            raise Http404

        if form.is_valid():
            data = form.save(commit=False)
            data.user = user
            data.updated_by = user
            data.save()
            # if not update add generic many-to-many relationship (gm2m)
            if not aid:
                date = data.date_created
                user.profile.applications.add(data)
            else:
                date = data.date_updated

            # email confirmation
            template = "application/email/%s.html" % application_type
            if not settings.DEBUG:
                TO_LIST.append(data.user.email)
                if aid:
                    app_name += " (UPDATED)"
                subject = "[%s] %s: %s, %s" % (
                    app_name, date,
                    data.user.last_name, data.user.first_name,
                )
                send_mail(
                    request, TO_LIST,
                    subject, data.user.email,
                    template, data, BCC,
                )
                return HttpResponseRedirect(reverse('application_success'))
            else:
                return render_to_response(
                    template,
                    {
                        'data': data,'form':form
                    },
                    context_instance=RequestContext(request)
                )

            return HttpResponseRedirect(reverse('application_success'))

    return render_to_response(
        "application/form.html",
        {"form": form,"app_name":app_name},
        context_instance=RequestContext(request)
    )

