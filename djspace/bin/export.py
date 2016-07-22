import django
django.setup()

from django.contrib.auth.models import User

users = User.objects.all().order_by("last_name")

for user in users:
    try:
        apps = user.profile.applications.all()
    except:
        apps = None
    if apps:
        for a in apps:
            #if str(a) == "First Nations Rocket Competition":
            if a.get_slug() == "first-nations-rocket-competition":
                print a.__dict__
