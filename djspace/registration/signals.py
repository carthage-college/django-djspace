from django.conf import settings
from django.db.models.signals import pre_save
from django.dispatch import receiver

from djspace.core.models import GenericChoice
from djspace.registration.models import Faculty
from djspace.registration.models import GrantsOfficer
from djspace.registration.models import Graduate
from djspace.registration.models import Undergraduate

from djtools.utils.mail import send_mail

'''
def _send_mail(obj, request, registration):
    """
    private function for sending an email
    """
    to_list = [settings.WSGC_EMAIL,settings.WSGC_APPLICATIONS]

    # send email to managers
    send_mail(
        request, to_list,
        "[WSGC {} Registration] Other Institute".format(registration),
        settings.SERVER_MAIL,
        'registration/email_wsgc_affiliate_other.html', obj,
        [settings.MANAGERS[0][1],]
    )


def _create_generic_choice(affiliate):
    """
    private function for creating a GenericChoice based on the name
    the user provided in the 'other' field for Institution/Organization
    """

    try:
        gc = GenericChoice.objects.get(name=affiliate)
    except:
        gc = GenericChoice(name=affiliate, value=affiliate, active=True)
        gc.save()
        gc.tags.add('College or University')

    return gc


@receiver(pre_save, sender=Faculty)
def registration_faculty_pre_save(sender, **kwargs):
    """
    Notify DevOps that a faculty has chosen 'Other' for Institution/Organization
    and that a new GenericChoice object has been created automatically
    based on the name provided in the wsgc_affiliate_other field
    """

    obj = kwargs['instance']
    if obj.wsgc_affiliate.name == 'Other':
        if obj.wsgc_affiliate_other:
            gc = _create_generic_choice(obj.wsgc_affiliate_other)
            obj.wsgc_affiliate_other = ''
            obj.wsgc_affiliate = gc

        _send_mail(obj, kwargs.get('request'), 'Faculty')


@receiver(pre_save, sender=GrantsOfficer)
def registration_grantsofficer_pre_save(sender, **kwargs):
    """
    Notify DevOps that a grants officer has chosen 'Other' for
    Institution/Organization and that a new GenericChoice object has been
    created automatically based on the name provided in the
    wsgc_affiliate_other field
    """

    obj = kwargs['instance']
    if obj.wsgc_affiliate.name == 'Other':
        if obj.wsgc_affiliate_other:
            gc = _create_generic_choice(obj.wsgc_affiliate_other)
            obj.wsgc_affiliate_other = ''
            obj.wsgc_affiliate = gc

        _send_mail(obj, kwargs.get('request'), 'Faculty')


@receiver(pre_save, sender=Undergraduate)
def registration_undergraduate_pre_save(sender, **kwargs):
    """
    Notify DevOps that an undergraduate has chosen 'Other' for Institution/Organization
    and that a new GenericChoice object has been created automatically
    based on the name provided in the wsgc_affiliate_other field
    """

    obj = kwargs['instance']
    if obj.wsgc_affiliate.name == 'Other':
        if obj.wsgc_affiliate_other:
            gc = _create_generic_choice(obj.wsgc_affiliate_other)
            obj.wsgc_affiliate_other = ''
            obj.wsgc_affiliate = gc

        _send_mail(obj, kwargs.get('request'), 'Undergraduate')


@receiver(pre_save, sender=Graduate)
def registration_graduate_pre_save(sender, **kwargs):
    """
    Notify DevOps that an graduate has chosen 'Other' for Institution/Organization
    and that a new GenericChoice object has been created automatically
    based on the name provided in the wsgc_affiliate_other field
    """

    obj = kwargs['instance']
    if obj.wsgc_affiliate.name == 'Other':
        if obj.wsgc_affiliate_other:
            gc = _create_generic_choice(obj.wsgc_affiliate_other)
            obj.wsgc_affiliate_other = ''
            obj.wsgc_affiliate = gc

        _send_mail(obj, kwargs.get('request'), 'Graduate')
'''
