# -*- coding: utf-8 -*-
from django.conf import settings
from django.db.models import Count
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required

from djspace.application.forms import *
from djspace.application.models import RocketLaunchTeam, ROCKET_COMPETITIONS
from djspace.registration.models import *
from djspace.core.utils import get_profile_status

from djtools.utils.mail import send_mail
from djtools.utils.convert import str_to_class

import logging
logger = logging.getLogger(__name__)


@login_required
def application_form(request, application_type, aid=None):

    # our user
    user = request.user

    # verify that the user has completed registration
    reg_type = user.profile.registration_type
    try:
        mod = str_to_class(
            "djspace.registration.models", reg_type
        )
        reg = mod.objects.get(user=user)
    except:
        # redirect to dashboard
        return HttpResponseRedirect(reverse('dashboard_home'))

    # verify that the user has an up to date registration
    if not get_profile_status(user):
        # redirect to dashboard
        return HttpResponseRedirect(reverse('dashboard_home'))

    # munge the application type
    slug_list = application_type.split("-")
    app_name = slug_list.pop(0).capitalize()
    for n in slug_list:
        app_name += " %s" % n.capitalize()
    app_type = "".join(app_name.split(" "))

    # check rocket competition teams and member limits.
    # currently, FNL does not have a limit so we can exclude it.
    if "rocket-competition" in application_type:
        teams = RocketLaunchTeam.objects.filter(
            competition__contains=app_name[:12]
        )

        if application_type != "first-nations-rocket-competition":
            teams = teams.annotate(
                count=Count('members')
            ).exclude(
                count__gte=settings.ROCKET_LAUNCH_COMPETITION_TEAM_LIMIT
            ).order_by("name")

        if not teams:
            return render_to_response(
                "application/form.html",
                {"form": None,"app_name":app_name},
                context_instance=RequestContext(request)
            )

    # email distribution
    if settings.DEBUG:
        TO_LIST = [settings.ADMINS[0][1],]
    else:
        TO_LIST = [settings.WSGC_APPLICATIONS,]

    # fetch object if update
    app = None
    # initialise work plan tasks for industry internship
    tasks = None
    if aid:
        mod = str_to_class(
            "djspace.application.models", app_type
        )

        if user.is_superuser:
            app = get_object_or_404(mod, pk=aid)
        else:
            # prevent users from managing apps that are not theirs
            try:
                app = mod.objects.get(pk=aid, user=user)
            except:
                app = None

    # fetch the form class
    FormClass = str_to_class(
        "djspace.application.forms", (app_type+"Form")
    )
    # fetch the form instance
    try:
        form = FormClass(instance=app)
    except:
        # app_type does not match an existing form
        raise Http404

    # GET or POST
    if request.method == 'POST':
        try:
            # only rocket launch team form needs request context
            if application_type == "rocket-launch-team":
                form = FormClass(
                    instance=app, data=request.POST, files=request.FILES,
                    request=request
                )
            else:
                form = FormClass(
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
            if application_type == "rocket-launch-team":
                # limit number of team members if need be
                if data.competition == "Midwest High-Powered Rocket Competition":
                    data.limit = 6
                else:
                    data.limit = 0
                data.save()
            # add user to RocketLaunchTeam member m2m
            if "rocket-competition" in application_type:
                data.team.members.add(data.user)

            # add work plan tasks for industry internship
            if application_type == "industry-internship":
                tid = request.POST.getlist('tid[]')
                title = request.POST.getlist('title[]')
                description = request.POST.getlist('description[]')
                percent = request.POST.getlist('hours_percent[]')
                expected_outcome = request.POST.getlist('expected_outcome[]')

                # remove deleted tasks
                task_list = [unicode(t.id) for t in data.work_plan_tasks.all()]
                dif = set(task_list).difference(tid)
                if len(dif) > 0:
                    for t in list(dif):
                        task = WorkPlanTask.objects.get(pk=int(t))
                        task.delete()
                # add or update tasks
                # len could use any of the above 5 lists from POST
                for i in range (0,len(tid)):
                    try:
                        task = WorkPlanTask.objects.get(pk=tid[i])
                    except:
                        task = WorkPlanTask()
                        task.industry_internship = data
                    task.title = title[i]
                    task.description = description[i]
                    task.hours_percent = percent[i]
                    task.expected_outcome = expected_outcome[i]
                    task.save()

            # if not update add generic many-to-many relationship (gm2m)
            if not aid:
                date = data.date_created
                user.profile.applications.add(data)
            else:
                date = data.date_updated

            # email confirmation
            template = "application/email/{}.html".format(application_type)
            if not settings.DEBUG:
                # send confirmation email to WSGC staff and applicant
                TO_LIST.append(data.user.email)
                if aid:
                    app_name += " (UPDATED)"
                subject = u"{} {}: {}, {}".format(
                    app_name, date,
                    data.user.last_name, data.user.first_name
                )
                send_mail(
                    request, TO_LIST,
                    subject, data.user.email,
                    template, data, settings.MANAGERS
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
    else:
        # set session values to null for GET requests
        request.session["leader_id"] = ""
        request.session["leader_name"] = ""
    return render_to_response(
        "application/form.html",
        {"form": form,"app_name":app_name,},
        context_instance=RequestContext(request)
    )

@staff_member_required
def application_print(request, application_type, aid):

    # munge the application type
    slug_list = application_type.split("-")
    app_name = slug_list.pop(0).capitalize()
    for n in slug_list:
        app_name += " %s" % n.capitalize()
    app_type = "".join(app_name.split(" "))

    mod = str_to_class(
        "djspace.application.models", app_type
    )
    data = get_object_or_404(mod, pk=aid)

    return render_to_response(
        "application/email/{}.html".format(application_type),
        {'data': data,},
        context_instance=RequestContext(request)
    )
