class EntityAlreadyExists(Exception):
    def __init__(self):
        self.message = "entity already exists"


class EntityNotFound(Exception):
    def __init__(self):
        self.message = "entity not found"


class InvalidEntity(Exception):
    def __init__(self, reason):
        self.message = "entity is invalid: {}".format(reason)


class InvalidRequest(Exception):
    def __init__(self, reason):
        self.message = "invalid request: {}".format(reason)