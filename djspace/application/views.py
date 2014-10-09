from django.conf import settings
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render_to_response, get_object_or_404

from djspace.application.forms import *

from djtools.utils.mail import send_mail


def form(request, reg_type):
    try:
        form = eval(reg_type.capitalize()+"Form")()
    except:
        raise Http404

    #template = "application/%s/form.html" % (reg_type),

    return render_to_response(
        "application/form.html",
        {"form": form,"reg_type":reg_type},
        context_instance=RequestContext(request)
    )
