import json

FILE_PATH = './static/store.json'


class Dao:
    def __init__(self):
        self._load_entities()

    def get_all(self):
        self._load_entities()
        return self.entities

    def get_entities_by_type(self, entity_type):
        self._load_entities()
        return self.entities.get(entity_type, [])

    def set_entities(self, entity_type, entities):
        self.entities[entity_type] = entities
        with open(FILE_PATH, 'w') as f:
            json.dump(self.entities, f)

    def _load_entities(self):
        with open(FILE_PATH) as f:
            self.entities = json.load(f)
