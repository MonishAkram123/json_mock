import constants
from exceptions import EntityAlreadyExists, EntityNotFound, InvalidEntity


class Controller:
    def __init__(self, dao):
        self.dao = dao
        pass

    def get_all(self):
        entities = self.dao.get_all()
        return entities

    def get_entities(self, entity_type, filter_args, sorting_args):
        entities = self.dao.get_entities_by_type(entity_type)
        result = list()
        for entity in entities:
            if self._is_matching_entity(entity, filter_args):
                result.append(entity)

        if sorting_args:
            reverse = sorting_args.get(constants.ORDER_KEY) == constants.ORDER_DESC
            sorting_key = sorting_args.get(constants.SORT_KEY)
            result = sorted(result, key=lambda obj: obj.get(sorting_key), reverse=reverse)

        return result

    def add_entities(self, entity_type, entities):
        self._validate_entities(entities)
        self.dao.set_entities(entity_type, entities)

    def get_entity(self, entity_type, entity_id):
        entities = self.dao.get_entities_by_type(entity_type)
        idx = self._find_entity_index_by_id(entities, entity_id)
        if idx is None:
            raise EntityNotFound()

        return entities[idx]

    def add_entity(self, entity_type, entity_id, new_entity):
        self._validate_entities([new_entity])

        if new_entity.get(constants.ID_KEY) != entity_id:
            raise InvalidEntity("id in body must match Id in request")

        entities = self.dao.get_entities_by_type(entity_type)
        idx = self._find_entity_index_by_id(entities, entity_id)
        if idx is not None:
            raise EntityAlreadyExists()

        entities.append(new_entity)
        self.dao.set_entities(entity_type, entities)

    def update_entity(self, entity_type, entity_id, new_entity):
        self._validate_entities([new_entity])

        entities = self.dao.get_entities_by_type(entity_type)
        idx = self._find_entity_index_by_id(entities, entity_id)
        if idx is None:
            raise EntityNotFound()

        entity = entities[idx]
        if entity.get(constants.ID_KEY) != new_entity.get(constants.ID_KEY):
            raise InvalidEntity("id is immutable")

        entities[idx] = new_entity
        self.dao.set_entities(entity_type, entities)

    def delete_entity(self, entity_type, entity_id):
        entities = self.dao.get_entities_by_type(entity_type)
        idx = self._find_entity_index_by_id(entities, entity_id)
        if idx is None:
            raise EntityNotFound()

        entities = entities[:idx] + entities[idx + 1:]
        self.dao.set_entities(entity_type, entities)

    @staticmethod
    def _is_matching_entity(entity, filter_args):
        if filter_args is None or len(filter_args) is 0:
            return True
        for key in filter_args:
            if filter_args[key] != entity.get(key):
                return False
        return True

    @staticmethod
    def _find_entity_index_by_id(entities, entity_id):
        for i in range(len(entities)):
            if entities[i].get(constants.ID_KEY) == entity_id:
                return i

    @staticmethod
    def _validate_entities(entities):
        ids = set()
        try:
            for entity in entities:
                entity_id = entity.get(constants.ID_KEY)
                assert entity_id is not None, "id is missing from {}".format(entity)
                assert type(entity_id) is int, "id is non-integer for {}".format(entity)
                assert entity_id not in ids, "duplicate id in: {}".format(entity)
                ids.add(entity_id)
        except AssertionError as e:
            raise InvalidEntity(e.message)
