from django.http import HttpResponse
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404

from djspace.dashboard.views import UPLOAD_FORMS
from djspace.core.forms import UserFilesForm
from djspace.core.models import UserFiles
from djspace.application.models import *

"""
@csrf_exempt
def user_files(request):

    user = request.user
    response = None
    valid="get"
    if request.method == "POST":
        valid="no"
        ct = request.POST.get("ct")
        ct = ContentType.objects.get(pk=ct)
        mod = ct.model_class()
        obj = mod.objects.get(pk=request.POST.get("oid"))
        form = UPLOAD_FORMS[ct.model](data=request.POST, files=request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            valid='yes'
        else:
            valid=form.errors
        return render_to_response(
                "dashboard/test.done.html", {
                "form":form,"valid":valid
            },
            context_instance=RequestContext(request)
        )
    else:
        ct = request.GET.get("ct")
        ct = ContentType.objects.get(pk=ct)
        mod = ct.model_class()
        obj = mod.objects.get(pk=request.GET.get("oid"))
        form = UPLOAD_FORMS[ct.model](instance=obj)
    return render_to_response(
        "dashboard/test.html", {
            "form":form,"valid":valid
        },
        context_instance=RequestContext(request)
    )
"""

@csrf_exempt
@login_required
def user_files(request):

    user = request.user
    response = None
    if request.method != "POST":
        msg = "POST required"
    else:
        ct = request.POST.get("content_type")
        if ct:
            ct = ContentType.objects.get(pk=ct)
            mod = ct.model_class()
            obj = mod.objects.get(pk=request.POST.get("oid"))
            # is someone being naughty?
            if obj.user != user:
                return HttpResponse(
                    "Something is rotten in Denmark",
                    content_type="text/plain; charset=utf-8"
                )
            else:
                form = UPLOAD_FORMS[ct.model](
                    data=request.POST, files=request.FILES, instance=obj
                )
        else:
            try:
                instance = UserFiles.objects.get(user=user)
            except:
                instance = None
            form = UserFilesForm(
                data=request.POST, files=request.FILES, instance=instance
            )
        if form.is_valid():
            phile = form.save(commit=False)
            if not ct:
                phile.user = user
            phile.save()
            field_name = request.POST.get("field_name")
            earl = getattr(phile,field_name)
            response = render_to_response(
                "dashboard/view_file.ajax.html", {
                    "earl":earl.url,"field_name":field_name
                },
                context_instance=RequestContext(request)
            )
        else:
            msg = "Fail"
            #msg = form.errors

    if not response:
        response = HttpResponse(
            msg, content_type="text/plain; charset=utf-8"
        )

    return response
