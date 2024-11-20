from game.item.inventory import Inventory
from json import dumps
from utils.json_encoder import QuestEncoder as q

class Character:
    def __init__(self, **kwargs):
        if "name" not in kwargs:
            kwargs["name"] = "Unnamed Character"
        if "description" not in kwargs:
            kwargs["description"] = "A character"
        if "location" not in kwargs:
            kwargs["location"] = "world_map"
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.inventory = Inventory(kwargs.get("inventory", []))

    def __repr__(self):
        return dumps(self.__dict__, indent=4, cls=q)

    def to_json(self):
        return self.__dict__
    