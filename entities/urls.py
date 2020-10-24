from django.conf.urls import url

from views import entity, entities, all

entity_type_pattern = '(?P<entity_type>[a-zA-Z]+)'
entity_id_pattern = '(?P<entity_id>[0-9]+)'


urlpatterns = [
    url(r'^' + entity_type_pattern + '$', entities),
    url(r'^' + entity_type_pattern + '/' + entity_id_pattern + '$', entity),
    url(r'^$', all),
]


