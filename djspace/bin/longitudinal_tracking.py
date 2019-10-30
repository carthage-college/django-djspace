'''
print('import')
import django
print('setup')
django.setup()

'''
from django.contrib.auth.models import User
from djspace.application.models import UndergraduateScholarship

print('fetch all users')
users = User.objects.all().order_by('last_name')
program = None
exports = []
print('begin users loop')
for user in users:
    try:
        apps = user.profile.applications.all()
    except:
        apps = None
    if apps:
        for a in apps:
            if a._meta.object_name == UndergraduateScholarship._meta.object_name and a.status:
                exports.append({'user':user,'app':a})
                program = a.get_slug()

print('longitudinal tracking')
print(exports)
