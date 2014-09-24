from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required

from djspace.registration.forms import *

@login_required
def form(request, reg_type):
    """
    Generic form method that handles all registration types.
    """
    user = request.user
    try:
        reg = eval(reg_type).object.get(user=user)
    except:
        reg = None
    try:
        form = eval(reg_type+"Form")(instance=reg)
    except:
        raise Http404
    if request.method == 'POST':
        try:
            form = eval(reg_type+"Form")(instance=reg, data=request.POST)
        except:
            raise Http404
        if form.is_valid():
            data = form.save(commit=False)
            data.user = user
            data.save()
            return HttpResponseRedirect(reverse('registration_success'))

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
