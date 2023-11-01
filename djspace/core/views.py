# -*- coding: utf-8 -*-

import mimetypes
import os


from django.conf import settings
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from djspace.application.models import *
from djspace.core.forms import EmailApplicantsForm
from djspace.core.forms import PhotoForm
from djspace.core.forms import UserFilesForm
from djspace.core.models import UserFiles
from djspace.core.utils import files_status
from djspace.dashboard.views import UPLOAD_FORMS
from djtools.utils.mail import send_mail


@staff_member_required
def sendmail(request):
    """Send emails to program applicants from admin action email_applicants."""
    redirect = request.META['HTTP_REFERER']
    if request.POST:
        # form stuff
        form = EmailApplicantsForm(request.POST, use_required_attribute=False)
        form.is_valid()
        cd = form.cleaned_data
        # content type
        ct = ContentType.objects.get_for_id(cd['content_type'])
        # program ids
        pids = request.POST.getlist('pids[]')
        # email subject
        sub = "WSGC: Information about your {0} application".format(
            cd['title'],
        )
        bcc = [request.user.email, settings.SERVER_MAIL]
        for pid in pids:
            instance = ct.get_object_for_this_type(pk=pid)
            to = [instance.user.email]
            send_mail(
                request,
                to,
                sub,
                settings.SERVER_EMAIL,
                'admin/email_data.html',
                {'obj': instance, 'content': cd.get('content')},
                bcc,
            )
        messages.add_message(
            request,
            messages.SUCCESS,
            'Your message was sent successfully.',
            extra_tags='success',
        )

    return HttpResponseRedirect(redirect)


@csrf_exempt
@login_required
def photo_upload(request):
    """AJAX POST for uploading a photo for any given application."""
    response = None
    if request.method == 'POST':
        form = PhotoForm(
            data=request.POST, files=request.FILES, use_required_attribute=False,
        )
        if form.is_valid():
            ct = request.POST.get('content_type')
            oid = request.POST.get('oid')
            if ct and oid:
                ct = ContentType.objects.get(pk=ct)
                mod = ct.model_class()
                try:
                    instance = mod.objects.get(pk=oid)
                    phile = form.save(commit=False)
                    phile.content_object = instance
                    phile.save()
                    response = render(
                        request,
                        'dashboard/view_photo.ajax.html',
                        {'photo': phile, 'ct': ct, 'oid': oid},
                    )
                except Exception as error:
                    msg = "Fail: {0}".format(str(error))
            else:
                msg = "Fail: No Content Type or Object ID Provided"
        else:
            msg = "Fail: {0}".format(form.errors)
    else:
        msg = "AJAX POST required"

    if not response:
        response = HttpResponse(msg, content_type='text/plain; charset=utf-8')

    return response


@csrf_exempt
@login_required
def user_files(request):
    """Update user and program files via ajax post."""
    user = request.user
    response = None
    if request.method == 'POST':
        ct = request.POST.get('content_type')
        if ct:
            ct = ContentType.objects.get(pk=ct)
            mod = ct.model_class()
            instance = mod.objects.get(pk=request.POST.get('oid'))
            # team leaders, co-advisors, and grants officers can upload files
            # for rocket launch teams and professional programs
            manager = False
            try:
                goid = instance.grants_officer.id
            except Exception:
                goid = None
            try:
                goid2 = instance.grants_officer2.id
            except Exception:
                goid2 = None
            try:
                coid1 = instance.co_advisor1.id
            except Exception:
                coid1 = None
            try:
                coid2 = instance.co_advisor2.id
            except Exception:
                coid2 = None
            try:
                coid3 = instance.co_advisor3.id
            except Exception:
                coid3 = None
            if ct.model == 'rocketlaunchteam':
                # this should be optimized
                if instance.leader.id == user.id or goid == user.id or goid2 == user.id or coid1 == user.id or coid2 == user.id or coid3 == user.id:
                    manager = True
            if ct.model in PROFESSIONAL_PROGRAMS:
                if goid == user.id or goid2 == user.id:
                    manager = True

            # is someone being naughty?
            if instance.user != user and not manager:
                return HttpResponse(
                    "Something is rotten in Denmark",
                    content_type='text/plain; charset=utf-8',
                )
            else:
                form = UPLOAD_FORMS[ct.model](
                    data=request.POST,
                    files=request.FILES,
                    instance=instance,
                    use_required_attribute=False,
                )
        else:
            try:
                instance = UserFiles.objects.get(user=user)
            except Exception:
                instance = None
            form = UserFilesForm(
                data=request.POST,
                files=request.FILES,
                instance=instance,
                use_required_attribute=False,
            )
        field_name = request.POST.get('field_name')
        if form.is_valid():
            if field_name:
                msg = "Success"
                phile = form.save(commit=False)
                if not ct:
                    phile.user = user
                phile.save()
                earl = getattr(phile, field_name)
                # notify wsgc that a user uploaded one of their files
                to = [settings.WSGC_EMAIL]
                to_list = None
                # send email to specific folks for various programs
                if ct and settings.FILE_UPLOADED_EMAILS.get(ct.model):
                    to.extend(settings.FILE_UPLOADED_EMAILS[ct.model])
                else:
                    to.extend(settings.FILE_UPLOADED_EMAILS['all'])
                if settings.DEBUG:
                    to_list = to
                    to = [settings.ADMINS[0][1]]
                subject = "[File Upload] {0}: {1}, {2}".format(
                    field_name, user.last_name, user.first_name,
                )
                bcc = [settings.SERVER_MAIL]
                # set up CC for WSGC folks for specific programs
                sent = send_mail(
                    request,
                    to,
                    subject,
                    user.email,
                    'dashboard/email_file_uploaded.html',
                    {
                        'earl': earl.url,
                        'obj': phile,
                        'field_name': field_name,
                        'to_list': to_list,
                        'userfiles': [
                            'mugshot', 'biography', 'irs_w9',
                        ],
                    },
                    bcc,
                )
                response = render(
                    request,
                    'dashboard/view_file.ajax.html',
                    {'earl': earl.url, 'field_name': field_name},
                )
            else:
                msg = "Fail: Field name is missing"
        else:
            msg = "Fail: {0}".format(form.errors)
    else:
        msg = "POST required"

    if not response:
        response = HttpResponse(msg, content_type='text/plain; charset=utf-8')
    return response


@csrf_exempt
@login_required
def check_files_status(request):
    """
    Determine if the user has all of her files uploaded or not.

    Method: ajax post
    Return: True or False
    """
    if request.method == 'POST':
        status = files_status(request.user)
    else:
        status = "POST required"

    return HttpResponse(status, content_type='text/plain; charset=utf-8')


@staff_member_required
def download_file(request, field, ct, oid, uid):
    """Download a file with a name that matches the program."""
    files = {
        'mugshot': 'Photo',
        'biography': 'Bio',
        'irs_w9': 'W9',
    }
    lackey = None
    if request.GET.get('lackey'):
        lackey = request.GET['lackey']
    user = User.objects.get(pk=uid)
    attr = getattr(user.user_files, field, None)
    path = os.path.join(settings.MEDIA_ROOT, attr.name)
    extension = path.split('.')[-1]
    ct = ContentType.objects.get(pk=ct)
    mod = ct.model_class()
    instance = mod.objects.get(pk=oid)
    filename = '{0}_{1}.{2}'.format(
        instance.get_file_name(lackey=lackey), files[field], extension,
    )
    with open(path, 'rb') as phile:
        mime_type, _ = mimetypes.guess_type(path)
        response = HttpResponse(phile, content_type=mime_type)
        response['Content-Disposition'] = 'attachment; filename={0}'.format(filename)
    return response


@csrf_exempt
def user_files_test(request):
    """Test for user file upload."""
    valid = 'get'
    if request.method == 'POST':
        valid = 'no'
        ct = request.POST.get('ct')
        ct = ContentType.objects.get(pk=ct)
        mod = ct.model_class()
        instance = mod.objects.get(pk=request.POST.get('oid'))
        form = UPLOAD_FORMS[ct.model](
            data=request.POST,
            files=request.FILES,
            instance=instance,
            use_required_attribute=False,
        )
        if form.is_valid():
            form.save()
            valid = 'yes'
        else:
            valid = form.errors
    else:
        ct = request.GET.get('ct')
        ct = ContentType.objects.get(pk=ct)
        mod = ct.model_class()
        instance = mod.objects.get(pk=request.GET.get('oid'))
        form = UPLOAD_FORMS[ct.model](
            instance=instance, use_required_attribute=False,
        )
    return render(
        request, 'dashboard/test.html', {'form': form, 'valid': valid},
    )


@csrf_exempt
@login_required
def object_delete(request):
    """AJAX POST for deleting arbitrary objects."""
    user = request.user
    if request.method == 'POST':
        try:
            # object ID
            oid = int(request.POST.get('oid'))
            # content type ID
            cid = int(request.POST.get('cid'))
            try:
                ct = ContentType.objects.get(pk=cid)
                mod = ct.model_class()
                try:
                    instance = mod.objects.get(pk=oid)
                    if ct.model == 'photo':
                        uid = instance.content_object.user.id
                    else:
                        uid = instance.user.id
                    # is someone doing something nefarious?
                    if uid == user.id or user.is_superuser:
                        instance.delete()
                        msg = "Success"
                    else:
                        msg = "Fail: Inadequate Permissions"
                except Exception as get_error:
                    msg = "Fail: {0}".format(str(get_error))
            except Exception as content_type_error:
                msg = "Fail: {0}".format(str(content_type_error))
        except Exception as error:
            msg = "Fail: {0}".format(str(error))
    else:
        msg = "AJAX POST required"

    return HttpResponse(msg, content_type="text/plain; charset=utf-8")
