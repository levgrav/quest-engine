import uuid

class MatchingIDsError(Exception):
    def __init__(self, id, *args):
        super().__init__(f"one or more GameObjects has the id '{id}'", *args)

class GameWorld:
    def __init__(self, game_objects = [], **kwargs):
        
        self.game_objects = game_objects
        self.test_thing = "hello world"
        
        self.assert_unique_ids()

        for key, value in kwargs:
            self.__setattr__(key, value)

    def assert_unique_ids(self):
        ids = []
        for o in self.game_objects:
            if o.id in ids:
                raise MatchingIDsError(o.id)
            else:
                ids.append(o.id)

class GameObject:
    def __init__(self, name, id = None, tags = [], relations = [], properties = [], **kwargs):
        self.name = name
        self.id = id if id != None else uuid.uuid4()
        self.tags = tags
        self.relations = relations
        self.properties = properties

        for key, value in kwargs:
            self.__setattr__(key, value)