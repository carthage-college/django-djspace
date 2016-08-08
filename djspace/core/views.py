from django.http import HttpResponse
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404

from djspace.core.forms import UserFilesForm
from djspace.core.models import UserFiles

import logging
logger = logging.getLogger(__name__)

@csrf_exempt
@login_required
def user_files(request):

    user = request.user
    try:
        instance = UserFiles.objects.get(user=user)
    except:
        instance = None
    if request.method != "POST":
        msg = "POST required"
    else:
        logger.debug("post = {}".format(request.FILES.__dict__))
        form = UserFilesForm(
            data=request.POST, files=request.FILES, instance=instance
        )
        if form.is_valid():
            phile = form.save(commit=False)
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

    if not response:
        response = HttpResponse(
            msg, content_type="text/plain; charset=utf-8"
        )

    return response

