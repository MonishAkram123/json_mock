from django.http.response import JsonResponse, HttpResponseBadRequest, HttpResponseNotFound, HttpResponse
import json

from constants import SORT_KEY, ORDER_KEY, ORDER_DESC, ORDER_ASC
from exceptions import EntityNotFound, EntityAlreadyExists, InvalidEntity, InvalidRequest

valid_orders = [ORDER_DESC, ORDER_ASC]
STATUS_CREATED = 201


class Handler:
    def __init__(self, controller):
        self.controller = controller

    def get_entity(self, entity_type, entity_id):
        try:
            entity_type = self._validate_and_get_entity_type(entity_type)
            entity_id = self._validate_and_get_entity_id(entity_id)
            entity = self.controller.get_entity(entity_type, entity_id)
            return JsonResponse(entity, safe=False)
        except AssertionError as e:
            return HttpResponseBadRequest(content=e.message)
        except EntityNotFound:
            return HttpResponseNotFound()

    def add_entity(self, entity_type, entity_id, body):
        try:
            entity_type = self._validate_and_get_entity_type(entity_type)
            entity_id = self._validate_and_get_entity_id(entity_id)
            entity = self._validate_body_and_get_entity(body)
            self.controller.add_entity(entity_type, entity_id, entity)
            return HttpResponse(status=STATUS_CREATED)
        except (AssertionError, EntityAlreadyExists, InvalidEntity) as e:
            return HttpResponseBadRequest(content=e.message)

    def update_entity(self, entity_type, entity_id, body):
        try:
            entity_type = self._validate_and_get_entity_type(entity_type)
            entity_id = self._validate_and_get_entity_id(entity_id)
            entity = self._validate_body_and_get_entity(body)
            self.controller.update_entity(entity_type, entity_id, entity)
            return HttpResponse(status=STATUS_CREATED)
        except (AssertionError, EntityNotFound, InvalidEntity) as e:
            return HttpResponseBadRequest(content=e.message)

    def delete_entity(self, entity_type, entity_id):
        try:
            entity_type = self._validate_and_get_entity_type(entity_type)
            entity_id = self._validate_and_get_entity_id(entity_id)
            self.controller.delete_entity(entity_type, entity_id)
            return HttpResponse()
        except (AssertionError, EntityNotFound) as e:
            return HttpResponseBadRequest(content=e.message)

    def get_entities_by_type(self, entity_type, params):
        try:
            entity_type = self._validate_and_get_entity_type(entity_type)
            filter_args, sorting_args = self._validate_and_get_filter_sorting_args(params)
            entities = self.controller.get_entities(entity_type, filter_args, sorting_args)
            return JsonResponse(entities, safe=False)
        except (AssertionError, InvalidRequest) as e:
            return HttpResponseBadRequest(content=e.message)

    def add_entities(self, entity_type, body):
        try:
            entity_type = self._validate_and_get_entity_type(entity_type)
            entities = self._validate_body_and_get_entities(body)
            self.controller.add_entities(entity_type, entities)
            return HttpResponse(status=STATUS_CREATED)
        except (AssertionError, InvalidEntity) as e:
            return HttpResponseBadRequest(content=e.message)

    @staticmethod
    def _validate_and_get_entity_type(entity_type):
        assert entity_type is not None, "entity_type is None"
        return str(entity_type)

    @staticmethod
    def _validate_and_get_entity_id(entity_id):
        assert entity_id is not None, "entity_id is None"
        try:
            return int(entity_id)
        except ValueError as e:
            raise AssertionError("entity_id is not of integer type")

    @staticmethod
    def _validate_body_and_get_entity(body):
        try:
            assert body is not None, "body is empty"
            entity = json.loads(body)
            assert type(entity) is dict, "body should be a json object with key-value pair"
            return entity
        except Exception as e:
            raise AssertionError(e.message)

    @staticmethod
    def _validate_body_and_get_entities(body):
        try:
            assert body is not None, "body is empty"
            entities = json.loads(body)
            assert type(entities) is list, "body should be a list of json object with key-value pair"
            for entity in entities:
                Handler._validate_body_and_get_entity(json.dumps(entity))
            return entities
        except Exception as e:
            raise AssertionError(e.message)

    @staticmethod
    def _validate_and_get_filter_sorting_args(params):
        filter_args, sorting_args = dict(), dict()
        sorting_keys = [SORT_KEY, ORDER_KEY]
        for key in params:
            key, value = str(key), str(params[key])
            if key in sorting_keys:
                sorting_args[key] = value
            else:
                filter_args[key] = value

        if sorting_args.get(SORT_KEY) is None and sorting_args.get(ORDER_KEY) is not None:
            raise InvalidRequest("sorting key is required if _order is given")

        if sorting_args.get(ORDER_KEY) is not None and sorting_args.get(ORDER_KEY) not in valid_orders:
            raise InvalidRequest("sorting order is not valid. must be either of: {}".format(valid_orders))

        if len(sorting_args) is 0:
            sorting_args = None

        return filter_args, sorting_args
