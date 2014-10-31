from django.conf import settings
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404

from djspace.application.forms import *

from djtools.utils.mail import send_mail

@login_required
def form(request, app_type, aid=None):
    user = request.user
    slist = app_type.split("-")
    app_name = slist.pop(0).capitalize()
    for n in slist:
        app_name += " %s" % n.capitalize()
    app_type = "".join(app_name.split(" "))

    app = None
    if aid:
        try:
            app = eval(app_type).objects.get(pk=aid, user=user)
        except:
            app = None

    try:
        form = eval(app_type+"Form")(instance=app)
    except:
        raise Http404

    if request.method == 'POST':
        try:
            form = eval(app_type+"Form")(
                instance=app, data=request.POST, files=request.FILES
            )
        except:
            raise Http404
        if form.is_valid():
            data = form.save(commit=False)
            data.user = user
            data.updated_by = user
            data.save()
            # if not update add generic many-to-many relationship (gm2m)
            if not aid:
                user.profile.applications.add(data)
            return HttpResponseRedirect(reverse('application_success'))

    return render_to_response(
        "application/form.html",
        {"form": form,"app_name":app_name},
        context_instance=RequestContext(request)
    )

