# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.shortcuts import get_object_or_404

from djspace.dashboard.views import UPLOAD_FORMS
from djspace.core.forms import PhotoForm, UserFilesForm
from djspace.core.forms import EmailApplicantsForm
from djspace.core.models import UserFiles
from djspace.core.utils import files_status
from djspace.application.models import *

from djtools.utils.mail import send_mail


@staff_member_required
def sendmail(request, redirect):
    """
    Send emails to program applicants.
    POST from admin action email_applicants.
    """

    redirect = '{}/{}'.format(settings.ROOT_URL, redirect)
    if request.POST:
        # form stuff
        form = EmailApplicantsForm(request.POST, use_required_attribute=False)
        form.is_valid()
        data = form.cleaned_data
        # content type
        ct = ContentType.objects.get_for_id(data['content_type'])
        # program ids
        pids = request.POST.getlist('pids[]')
        # email subject
        sub = "WSGC: Information about your {} application".format(
            data['title']
        )
        bcc = [request.user.email,settings.SERVER_MAIL]
        for pid in pids:
            obj = ct.get_object_for_this_type(pk=pid)
            to = [obj.user.email]
            send_mail(
                request, to, sub, settings.SERVER_EMAIL,
                'admin/email_data.html',
                {'obj':obj,'content':data['content']}, bcc
            )
        messages.add_message(
            request, messages.SUCCESS,
            'Your message was sent successfully.',
            extra_tags='success'
        )
        return HttpResponseRedirect(redirect)
    else:
        return HttpResponseRedirect(redirect)


@csrf_exempt
@login_required
def photo_upload(request):
    """
    AJAX POST for uploading a photo for any given application
    """

    user = request.user
    response = None
    if request.is_ajax() and request.method == 'POST':
        form = PhotoForm(
            data=request.POST, files=request.FILES, use_required_attribute=False
        )
        if form.is_valid():
            ct = request.POST.get('content_type')
            oid = request.POST.get('oid')
            if ct and oid:
                ct = ContentType.objects.get(pk=ct)
                mod = ct.model_class()
                try:
                    obj = mod.objects.get(pk=oid)
                    phile = form.save(commit=False)
                    phile.content_object = obj
                    phile.save()
                    response = render(
                        request, 'dashboard/view_photo.ajax.html', {
                            'photo':phile,'ct':ct,'oid':oid
                        }
                    )
                except Exception, e:
                    msg = "Fail: {}".format(str(e))
            else:
                msg = "Fail: No Content Type or Object ID Provided"
        else:
            msg = "Fail: {}".format(form.errors)
    else:
        msg = "AJAX POST required"

    if not response:
        response = HttpResponse(
            msg, content_type='text/plain; charset=utf-8'
        )

    return response


@csrf_exempt
@login_required
def user_files(request):
    """
    update user files via ajax post
    """
    user = request.user
    response = None
    if request.method != 'POST':
        msg = "POST required"
    else:
        ct = request.POST.get('content_type')
        if ct:
            ct = ContentType.objects.get(pk=ct)
            mod = ct.model_class()
            obj = mod.objects.get(pk=request.POST.get('oid'))

            # team leaders, co-advisors, and grants officers can upload files
            # for rocket launch teams and professional programs
            manager = False
            if ct.model == 'rocketlaunchteam':
                if obj.leader.id == user.id or obj.co_advisor.id == user.id or \
                  obj.grants_officer.id == user.id:
                    manager = True
            if ct.model in PROFESSIONAL_PROGRAMS:
                if obj.grants_officer.id == user.id:
                    manager = True

            # is someone being naughty?
            if obj.user != user and not manager:
                return HttpResponse(
                    "Something is rotten in Denmark",
                    content_type='text/plain; charset=utf-8'
                )
            else:
                form = UPLOAD_FORMS[ct.model](
                    data=request.POST, files=request.FILES, instance=obj,
                    use_required_attribute=False
                )
        else:
            try:
                obj = UserFiles.objects.get(user=user)
            except:
                obj = None
            form = UserFilesForm(
                data=request.POST, files=request.FILES, instance=obj,
                use_required_attribute=False
            )
        field_name = request.POST.get('field_name')
        if form.is_valid():
            if field_name:
                msg = "Success"
                phile = form.save(commit=False)
                if not ct:
                    phile.user = user
                phile.save()
                earl = getattr(phile,field_name)
                # notify wsgc that a user uploaded one of her profile files
                if settings.DEBUG:
                    to = [settings.ADMINS[0][1],]
                else:
                    to = [settings.WSGC_EMAIL,]
                subject = u"[File Upload] {}: {}, {}".format(
                    field_name, user.last_name, user.first_name
                )
                bcc = [settings.SERVER_MAIL]
                send_mail(
                    request, to, subject, user.email,
                    'dashboard/email_file_uploaded.html', {
                        'earl':earl.url, 'obj':phile, 'field_name':field_name,
                        'userfiles':['mugshot','biography','irs_w9','media_release']
                    }, bcc
                )
                response = render(
                    request, 'dashboard/view_file.ajax.html', {
                        'earl':earl.url,'field_name':field_name
                    }
                )
            else:
                msg = "Fail: Field name is missing"
        else:
            msg = "Fail: {}".format(form.errors)

    if not response:
        response = HttpResponse(
            msg, content_type='text/plain; charset=utf-8'
        )
    return response


@csrf_exempt
@login_required
def check_files_status(request):
    """
    Determine if the user has all of her files uploaded or not.
    Method: ajax post
    Return: True or False
    """
    user = request.user
    response = None
    if request.method != 'POST':
        status = "POST required"
    else:
        status = files_status(request.user)

    return HttpResponse(
        status, content_type='text/plain; charset=utf-8'
    )


@csrf_exempt
def user_files_test(request):

    user = request.user
    response = None
    valid='get'
    if request.method == 'POST':
        valid='no'
        ct = request.POST.get('ct')
        ct = ContentType.objects.get(pk=ct)
        mod = ct.model_class()
        obj = mod.objects.get(pk=request.POST.get('oid'))
        form = UPLOAD_FORMS[ct.model](
            data=request.POST, files=request.FILES, instance=obj,
            use_required_attribute=False
        )
        if form.is_valid():
            form.save()
            valid='yes'
        else:
            valid=form.errors
    else:
        ct = request.GET.get('ct')
        ct = ContentType.objects.get(pk=ct)
        mod = ct.model_class()
        obj = mod.objects.get(pk=request.GET.get('oid'))
        form = UPLOAD_FORMS[ct.model](instance=obj, use_required_attribute=False)
    return render(
        request, 'dashboard/test.html', {'form':form, 'valid':valid}
    )


@csrf_exempt
@login_required
def object_delete(request):
    """
    AJAX POST for deleting arbitrary objects
    """
    user = request.user
    response = None
    if request.is_ajax() and request.method == 'POST':
        try:
            # object ID
            oid = int(request.POST.get('oid'))
            # content type ID
            cid = int(request.POST.get('cid'))
            try:
                ct = ContentType.objects.get(pk=cid)
                mod = ct.model_class()
                try:
                    obj = mod.objects.get(pk=oid)
                    # user id might come from object.user.id or from
                    # a custom method that returns the user object
                    try:
                        uid = obj.user.id
                    except:
                        uid = obj.user().id
                    # is someone doing something nefarious?
                    if oid == user.id or user.is_superuser:
                        obj.delete()
                        msg = "Success"
                    else:
                        msg = "Fail: Inadequate Permissions"
                except Exception, e:
                    msg = "Fail: {}".format(str(e))
            except Exception, e:
                    msg = "Fail: {}".format(str(e))
        except Exception, e:
            msg = "Fail: {}".format(str(e))
    else:
        msg = "AJAX POST required"

    return HttpResponse(
        msg, content_type="text/plain; charset=utf-8"
    )
