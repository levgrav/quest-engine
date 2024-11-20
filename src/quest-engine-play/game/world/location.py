from game.item.inventory import Inventory
from json import dumps
from utils.json_encoder import QuestEncoder as q

class Location:
    def __init__(self, **kwargs):
        self.name = kwargs.get("name", "Location")
        self.description = kwargs.get("description", "A location")
        self.features = kwargs.get("features", [])
        self.locations = kwargs.get("locations", [])
        self.routes = kwargs.get("routes", {})
        self.inventory = kwargs.get("inventory", Inventory())
    
    def __repr__(self):
        return dumps(self.__dict__, indent=4, cls=q)
    
    def to_json(self):
        return self.__dict__
    
