from django.http import HttpResponseNotAllowed
from constants import METHOD_DELETE, METHOD_GET, METHOD_PATCH, METHOD_POST, METHOD_PUT
from handler import Handler
from controller import Controller
from dao import Dao
from django.views.decorators.csrf import csrf_exempt

controller = Controller(Dao())
handler = Handler(controller)


@csrf_exempt
def entity(request, entity_type, entity_id):
    if request.method == METHOD_GET:
        return handler.get_entity(str(entity_type), int(entity_id))

    if request.method == METHOD_PUT:
        return handler.add_entity(entity_type, entity_id, request.body)

    if request.method == METHOD_PATCH:
        return handler.update_entity(entity_type, entity_id, request.body)

    if request.method == METHOD_DELETE:
        return handler.delete_entity(entity_type, entity_id)

    return HttpResponseNotAllowed("")


@csrf_exempt
def entities(request, entity_type):
    if request.method == METHOD_GET:
        return handler.get_entities_by_type(entity_type, request.GET)

    if request.method == METHOD_POST:
        return handler.add_entities(entity_type, request.body)

    return HttpResponseNotAllowed("")
