from django.conf.urls import url

from views import entity, entities

entity_type_pattern = '(?P<entity_type>[a-zA-Z]+)'
entity_id_pattern = '(?P<entity_id>[0-9]+)'


urlpatterns = [
    url(entity_type_pattern + '$', entities),
    url(entity_type_pattern + '/' + entity_id_pattern + '$', entity),
]


