import django
django.setup()

from django.conf import settings

from djspace.application.models import AerospaceOutreach

import tarfile

tar_ball = tarfile.open('aso.tar.gz', 'w:gz')

queryset = AerospaceOutreach.objects.all()

for obj in queryset:
    fotos = obj.photos.all()
    for i in range(len(fotos)):
        path = '{}/{}'.format(settings.MEDIA_ROOT, str(fotos[i].phile))
        path_list = path.split('/')
        name = '{}_{}_{}'.format(obj.id, i, path_list[-1])
        print(name)
        tar_ball.add(path, name)

tar_ball.close()
