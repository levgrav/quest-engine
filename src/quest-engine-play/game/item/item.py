from json import dumps
from utils.json_encoder import QuestEncoder as q

class Item:
    def __init__(self, **kwargs):
        if "name" not in kwargs:
            kwargs["name"] = "Unnamed Item"
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def __repr__(self):
        return dumps(self.__dict__, indent=4, cls=q)
    
    def to_json(self):
        return self.__dict__