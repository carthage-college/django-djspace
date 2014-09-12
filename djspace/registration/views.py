from django.conf import settings
from django.template import RequestContext
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render_to_response, get_object_or_404

from djspace.registration.forms import *

from djtools.utils.mail import send_mail


def form(request, reg_type):
    try:
        form = eval(reg_type.capitalize()+"Form")()
    except:
        raise Http404

    #template = "registration/%s/form.html" % (reg_type),
    
    return render_to_response(
        "registration/form.html",
        {"form": form,"reg_type":reg_type},
        context_instance=RequestContext(request)
    )


def undergrad(request):
    form = UndergraduateForm()

    return render_to_response(
        "registration/form.html",
        {"form": form,},
        context_instance=RequestContext(request)
    )

def graduate(request):
    form = GraduateForm()

    return render_to_response(
        "registration/form.html",
        {"form": form,},
        context_instance=RequestContext(request)
    )

def professional(request):
    form = ProfessionalForm()

    return render_to_response(
        "registration/form.html",
        {"form": form,},
        context_instance=RequestContext(request)
    )

def professor(request):
    form = ProfessorForm()

    return render_to_response(
        "registration/form.html",
        {"form": form,},
        context_instance=RequestContext(request)
    )

def k12educator(request):
    form = K12EducatorForm()

    return render_to_response(
        "registration/form.html",
        {"form": form,},
        context_instance=RequestContext(request)
    )
