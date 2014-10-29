from django.conf import settings
from django.template import RequestContext
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404

from djspace.application.forms import *

from djtools.utils.mail import send_mail

@login_required
def form(request, app_type):
    slist = app_type.split("-")
    app_name = slist.pop(0).capitalize()
    for n in slist:
        app_name += " %s" % n.capitalize()
    app_type = "".join(app_name.split(" "))

    try:
        form = eval(app_type+"Form")()
    except:
        raise Http404

    #template = "application/%s/form.html" % (app_type),

    return render_to_response(
        "application/form.html",
        {"form": form,"app_name":app_name},
        context_instance=RequestContext(request)
    )
