import django
django.setup()

from django.contrib.contenttypes.models import ContentType

from djspace.application.models import *
from djspace.dashboard.views import UPLOAD_FORMS

'''
obj = UndergraduateResearch.objects.get(pk=30)
ct = obj.get_content_type()
print ct.__dict__
m=obj.get_content_type().model
print m
form = APPLICATION_FORMS[m](instance=obj)
print form.as_p()
'''

ct = ContentType.objects.get(pk=32)
print ct
mod = ct.model_class()
print "name = {}".format( mod.model)
obj = mod.objects.get(pk=55)
print obj
form = UPLOAD_FORMS[ct.model](instance=obj)
print "form as p = {}".format(form.as_p())

