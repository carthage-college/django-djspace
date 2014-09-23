from django.core import serializers

from djspace.core.models import GenericChoice

from taggit.models import Tag, TaggedItem

#with open("generic_choice.json", "w") as out:
#with open("tag.json", "w") as out:
with open("tagged_item.json", "w") as out:
    json_serializer = serializers.get_serializer('json')()
    #json_serializer.serialize(GenericChoice.objects.all(), stream=out)
    #json_serializer.serialize(Tag.objects.all(), stream=out)
    json_serializer.serialize(TaggedItem.objects.all(), stream=out)

