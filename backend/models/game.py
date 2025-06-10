class Player:
    def __init__(self, name: str):
        self.name = name
        self.location = "starting room"
        self.inventory = []

class GameWorld:
    def __init__(self):
        self.rooms = {
            "starting room": "You are in a dimly lit stone chamber.",
            "forest": "You are surrounded by towering trees."
        }
