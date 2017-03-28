# -*- coding: utf-8 -*-
from django.conf import settings
from django.db.models import Count
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.template import loader, Context, RequestContext
from django.http import HttpResponse, HttpResponseRedirect, Http404

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required

from djspace.application.forms import *
from djspace.application.models import ROCKET_LAUNCH_COMPETITION_WITH_LIMIT
from djspace.core.models import UserFiles
from djspace.core.forms import UserFilesForm
from djspace.core.utils import profile_status
from djspace.core.utils import get_start_date

from djtools.fields.helpers import handle_uploaded_file
from djtools.utils.convert import str_to_class
from djtools.utils.mail import send_mail
from djtools.fields import TODAY

import django
from os.path import join

@login_required
def application_form(request, application_type, aid=None):

    # our user
    user = request.user
    # userfiles
    try:
        userfiles = UserFiles.objects.get(user=user)
    except:
        userfiles = None
    # UserFilesForm
    form_user_files = None

    # verify that the user has completed registration
    reg_type = user.profile.registration_type
    try:
        mod = django.apps.apps.get_model(
            app_label='registration', model_name=reg_type
        )
        reg = mod.objects.get(user=user)
    except:
        # redirect to dashboard
        return HttpResponseRedirect(reverse('dashboard_home'))

    # verify that the user has an up to date registration
    if not profile_status(user):
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
            return render(
                request, "application/form.html",
                {"form": None,"app_name":app_name}
            )

    # we need the application model now and if it barfs
    # we throw a 404
    try:
        mod = django.apps.apps.get_model(
            app_label='application', model_name=app_type
        )
    except:
        raise Http404

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

        if user.is_superuser:
            app = get_object_or_404(mod, pk=aid)
        else:
            # prevent users from managing apps that are not theirs
            try:
                app = mod.objects.get(pk=aid, user=user)
            except:
                return HttpResponseRedirect(reverse('dashboard_home'))


        # verify that create_date is after grant cycle began
        # otherwise redirect to dashboard home
        if app.date_created < get_start_date():
            # redirect to dashboard
            return HttpResponseRedirect(reverse('dashboard_home'))

    # rocket launch team co-advisor
    coa_orig = None
    if app and application_type == "rocket-launch-team":
        if app.co_advisor:
            # for autocomplete form field at the UI level
            request.session['co_advisor_name'] = u'{}, {}'.format(
                app.co_advisor.last_name, app.co_advisor.first_name
            )
            request.session['leader_name'] = u'{}, {}'.format(
                app.leader.last_name, app.leader.first_name
            )
            # we want to remove the old advisor if a new one is submitted
            # and add the new one to the application gm2m relationship
            coa_orig = app.co_advisor

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
            # rocket launch team and professional program student
            # forms need request context
            if application_type == "rocket-launch-team" or \
               application_type == "professional-program-student":
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

        # professional program student has three files from UserFiles
        if application_type == "professional-program-student":
            form_user_files = UserFilesForm(
                instance=userfiles,
                data=request.POST, files=request.FILES
            )
        if form.is_valid():

            if application_type == "professional-program-student":
                if form_user_files.is_valid():
                    form_user_files.save()
                else:
                    return render(
                        request, 'application/form.html', {
                            'form': form,'app_name':app_name,'obj':app,
                            'form_user_files':form_user_files
                        }
                    )

            data = form.save(commit=False)
            data.user = user
            data.updated_by = user

            if application_type == "rocket-launch-team":
                # limit number of team members if need be
                if data.competition in ROCKET_LAUNCH_COMPETITION_WITH_LIMIT:
                    data.limit = settings.ROCKET_LAUNCH_COMPETITION_TEAM_LIMIT
                else:
                    data.limit = 0

            # save media_release file to UserProfileFiles if first nations
            if application_type == "first-nations-rocket-competition":
                if request.FILES.get('media_release'):
                    try:
                        uf = user.user_files
                    except:
                        uf = UserFiles(user=user)
                    file_root = "{}/{}/{}/".format(
                        uf.get_file_path(),
                        uf.get_slug(),
                        str(user.id)
                    )
                    path = join(
                        settings.MEDIA_ROOT,
                        file_root
                    )
                    media_release = handle_uploaded_file(
                        request.FILES['media_release'], path,
                        u"{}_media_release".format(uf.get_file_name())
                    )
                    uf.media_release = u"{}{}".format(
                        file_root, media_release
                    )
                    uf.save()

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

            # if we have a rocket launch team application
            # add co-advisor to generic many-to-many relationsip (gm2m) if new
            # and remove the old one if need be
            if application_type == "rocket-launch-team":
                coa = data.co_advisor
                # we have a co-advisor, check if the old matches new
                if (coa_orig and coa) and coa.id != coa_orig.id:
                    # update
                    coa.profile.applications.add(data)
                    # delete the old co-advisor
                    coa_orig.profile.applications.remove(data)
                elif coa_orig and not coa:
                    # delete the old co-advisor because they removed
                    # the co-advisor from the field
                    coa_orig.profile.applications.remove(data)
                elif coa and not coa_orig:
                    # new application or new co-advisor on update
                    coa.profile.applications.add(data)

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
                return render(
                    request, template,
                    {'data': data,'form':form}
                )

            return HttpResponseRedirect(reverse('application_success'))
    else:
        # UserFilesForm
        form_user_files = UserFilesForm(instance=userfiles)
        if not app:
            # set session values to null for GET requests that are not updates
            request.session["leader_id"] = ""
            request.session["leader_name"] = ""
            request.session["co_advisor_id"] = ""
            request.session["co_advisor_name"] = ""
    return render(
        request, 'application/form.html', {
            'form': form,'app_name':app_name,'obj':app,
            'form_user_files':form_user_files
        }
    )


@staff_member_required
def application_print(request, application_type, aid):

    # munge the application type
    slug_list = application_type.split("-")
    app_name = slug_list.pop(0).capitalize()
    for n in slug_list:
        app_name += " %s" % n.capitalize()
    app_type = "".join(app_name.split(" "))

    mod = django.apps.apps.get_model(
        app_label='application', model_name=app_type
    )
    #data.reg = get_object_or_404(mod, pk=aid)
    data = get_object_or_404(mod, pk=aid)

    return render(
        request, "application/email/{}.html".format(application_type),
        {'data': data,}
    )


@staff_member_required
def application_export(request, application_type):
    users = User.objects.all().order_by("last_name")

    exports = []
    for user in users:
        try:
            apps = user.profile.applications.all()
        except:
            apps = None
        if apps:
            for a in apps:
                if a.get_slug() == application_type:
                    exports.append({"user":user,"app":a})
                    program = a.get_application_type()

    if settings.DEBUG:
        response = render(
            request, "application/export.html",
            {'exports': exports,'program':program,'year':TODAY.year},
            content_type="text/plain; charset=utf-8"
        )
    else:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="{}.csv"'.format(
            application_type
        )

        t = loader.get_template('application/export.html')
        c = Context({
            'exports': exports,
            'program':program,
            'year':TODAY.year
        })
        response.write(t.render(c))

    return response
