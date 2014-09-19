from django.conf import settings
from django.template import RequestContext, loader
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse, reverse_lazy
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

    if request.method == 'POST':
        form = UndergraduateForm(request.POST)
        if form.is_valid():
            #data = form.save(commit=False)
            return HttpResponseRedirect(reverse('success'))
        else:
            return render_to_response(
                "registration/form.html",
                {"form": form,"reg_type":"Undergraduate"},
                context_instance=RequestContext(request)
            )
    else:
        form = UndergraduateForm()
    return render_to_response(
        'registration/form.html',
        {'form': form,"reg_type":"Undergraduate"},
        context_instance=RequestContext(request)
    )


def graduate(request):

    if request.method == 'POST':
        form = GraduateForm(request.POST)
        if form.is_valid():
            #data = form.save(commit=False)
            return HttpResponseRedirect(reverse('success'))
        else:
            return render_to_response(
                "registration/form.html",
                {"form": form,"reg_type":"Graduate"},
                context_instance=RequestContext(request)
            )
    else:
        form = GraduateForm()
    return render_to_response(
        'registration/form.html',
        {'form': form,"reg_type":"Graduate"},
        context_instance=RequestContext(request)
    )


def professional(request):

    if request.method == 'POST':
        form = ProfessionalForm(request.POST)
        if form.is_valid():
            #data = form.save(commit=False)
            return HttpResponseRedirect(reverse('success'))
        else:
            return render_to_response(
                "registration/professional_form.html",
                {"form": form,"reg_type":"Professional"},
                context_instance=RequestContext(request)
            )
    else:
        form = ProfessionalForm()
    return render_to_response(
        'registration/professional_form.html',
        {'form': form,"reg_type":"Professional"},
        context_instance=RequestContext(request)
    )


def professor(request):

    if request.method == 'POST':
        form = FacultyForm(request.POST)
        if form.is_valid():
            #data = form.save(commit=False)
            return HttpResponseRedirect(reverse('success'))
        else:
            return render_to_response(
                "registration/faculty_form.html",
                {"form": form,"reg_type":"Faculty"},
                context_instance=RequestContext(request)
            )
    else:
        form = FacultyForm()
    return render_to_response(
        'registration/faculty_form.html',
        {'form': form,"reg_type":"Faculty"},
        context_instance=RequestContext(request)
    )