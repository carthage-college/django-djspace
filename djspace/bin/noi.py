import django
django.setup()

from djspace.application.models import RocketLaunchTeam

noi = RocketLaunchTeam.objects.get(pk=177)
print(noi)
print(noi.leader)

#for c in noi.collegiaterocketcompetition_set.all():
for c in noi.collegiate_rocket_competition.all():
    if c.user == noi.leader:
        print(c.award_acceptance)

