import django

django.setup()

from django.contrib.auth.models import User

users = User.objects.all().order_by("last_name")
program = None
exports = []

for user in users:
    try:
        apps = user.profile.applications.all()
    except:
        apps = None

    if apps:
        for a in apps:
            #print a
            print a.__dict__
            #print a._state.__dict__
            #print a.id
            # don't work
            #             #print a.all()
            #                         #print a.get_related_models()
