import django
django.setup()

from djspace.core.models import GenericManyToMany

"""
uncomment out the GenericManyToMany() model class
in core.models
"""

gs = GenericManyToMany.objects.all()
for g in gs:
    sources_pks = []
    count = 0
    sources = GenericManyToMany.objects.filter(
        gm2m_src__id=g.gm2m_src.id
    ).filter(gm2m_ct__id=g.gm2m_ct.id)
    for s in sources:
        sources_pks.append(s.gm2m_pk)
    for pk in sources_pks:
        if g.gm2m_pk == pk:
            count += 1
    if count > 1:
        print count, g.id
