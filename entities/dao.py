import json


class Dao:
    def __init__(self):
        with open('./store.json') as f:
            self.entities = json.load(f)

    def get_all(self):
        return self.entities

    def get_entities_by_type(self, entity_type):
        return self.entities.get(entity_type, [])

    def set_entities(self, entity_type, entities):
        self.entities[entity_type] = entities
        with open('./store.json', 'w') as f:
            json.dump(self.entities, f)
