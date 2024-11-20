from game.world.location import Location
from game.character.character import Character
from game.item.inventory import Inventory
from game.item.item import Item
from json import dumps
from utils.json_encoder import QuestEncoder as q

class World():
    def __init__(self):
        self.players = [Character(
            name="harold",
            description="A player character",
            location="world_map/forest/forest_clearing"
        )]
        self.npcs = [
            Character(name="npc1", location="world_map/forest"), 
            Character(name="npc2", location="world_map/mountain"),
        ]
        self.world_map = Location(
            name="World Map",
            description="The world map",
            features=["forest", "mountain", "river"],
            locations=[
                Location(
                    name="forest",
                    description="A forest",
                    features=["trees", "animals"],
                    locations=[
                        Location(
                            name="Forest Clearing",
                            description="A clearing in the forest",
                            features=["grass", "flowers"],
                            inventory=Inventory([
                                {'item':Item(name="Sword", description="A sword", value=10, weight=5), 'quantity': 1},
                                {'item':Item(name="Shield", description="A shield", value=10, weight=5), 'quantity': 1},
                                {'item':Item(name="Potion", description="A potion", value=10, weight=5), 'quantity': 1},
                            ])
                        )
                    ],
                    inventory=Inventory([
                        {'item':Item(name="Apple", description="An apple", value=1, weight=1), 'quantity': 1},
                        {'item':Item(name="Orange", description="An orange", value=1, weight=1), 'quantity': 1},
                        {'item':Item(name="Banana", description="A banana", value=1, weight=1), 'quantity': 1},
                    ])
                ),
                Location(
                    name="Mountain",
                    description="A mountain",
                    features=["rocks", "snow"],
                    locations=[
                        Location(
                            name="Mountain Cave",
                            description="A cave in the mountain",
                            features=["darkness", "bats"],
                            inventory=Inventory([
                                {'item':Item(name="Torch", description="A torch", value=10, weight=5), 'quantity': 1},
                                {'item':Item(name="Rope", description="A rope", value=10, weight=5), 'quantity': 1},
                                {'item':Item(name="Pickaxe", description="A pickaxe", value=10, weight=5), 'quantity': 1},
                            ])
                        ),
                        Location(
                            name="Mountain Peak",
                            description="The peak of the mountain",
                            features=["wind", "view"],
                            inventory=Inventory([
                                {'item':Item(name="Climbing Gear", description="Climbing gear", value=10, weight=5), 'quantity': 1},
                                {'item':Item(name="Oxygen Tank", description="Oxygen tank", value=10, weight=5), 'quantity': 1},
                                {'item':Item(name="Map", description="A map", value=10, weight=5), 'quantity': 1},
                            ])
                        ),
                        Location(
                            name="Monestary",
                            description="A monestary",
                            features=["monks", "prayer"],
                            locations=[
                                Location(
                                    name="Monestary Garden",
                                    description="A garden in the monestary",
                                    features=["flowers", "statues"],
                                    inventory=Inventory([
                                        {'item':Item(name="Herbs", description="Herbs", value=10, weight=5), 'quantity': 1},
                                        {'item':Item(name="Flowers", description="Flowers", value=10, weight=5), 'quantity': 1},
                                        {'item':Item(name="Statue", description="A statue", value=10, weight=5), 'quantity': 1},
                                    ])
                                ),
                                Location(
                                    name="Monestary Library",
                                    description="A library in the monestary",
                                    features=["books", "scrolls"],
                                    inventory=Inventory([
                                        {'item':Item(name="Book", description="A book", value=10, weight=5), 'quantity': 1},
                                        {'item':Item(name="Scroll", description="A scroll", value=10, weight=5), 'quantity': 1},
                                        {'item':Item(name="Quill", description="A quill", value=10, weight=5), 'quantity': 1},
                                    ])
                                ),
                                Location(
                                    name="Monestary Dormitory",
                                    description="A dormitory in the monestary",
                                    features=["beds", "clothes"],
                                    inventory=Inventory([
                                        {'item':Item(name="Bed", description="A bed", value=10, weight=5), 'quantity': 1},
                                        {'item':Item(name="Clothes", description="Clothes", value=10, weight=5), 'quantity': 1},
                                        {'item':Item(name="Blanket", description="A blanket", value=10, weight=5), 'quantity': 1},
                                    ])
                                )
                            ],
                            inventory=Inventory([
                                {'item':Item(name="Monk Robes", description="Monk robes", value=10, weight=5), 'quantity': 1},
                                {'item':Item(name="Prayer Beads", description="Prayer beads", value=10, weight=5), 'quantity': 1},
                                {'item':Item(name="Candle", description="A candle", value=10, weight=5), 'quantity': 1},
                            ])
                        )
                    ],
                    inventory=Inventory([
                        {'item':Item(name="Rock", description="A rock", value=1, weight=1), 'quantity': 1},
                        {'item':Item(name="Snowball", description="A snowball", value=1, weight=1), 'quantity': 1},
                        {'item':Item(name="Ice", description="Ice", value=1, weight=1), 'quantity': 1},
                    ])
                ),
                Location(
                    name="River",
                    description="A river",
                    features=["water", "fish"],
                    locations=[
                        Location(
                            name="River Bank",
                            description="The bank of the river",
                            features=["mud", "reeds"],
                            inventory=Inventory([
                                {'item':Item(name="Fishing Rod", description="A fishing rod", value=10, weight=5), 'quantity': 1},
                                {'item':Item(name="Bait", description="Bait", value=10, weight=5), 'quantity': 1},
                                {'item':Item(name="Net", description="A net", value=10, weight=5), 'quantity': 1},
                            ])
                        ),
                        Location(
                            name="River Crossing",
                            description="A crossing on the river",
                            features=["bridge", "rocks"],
                            inventory=Inventory([
                                {'item':Item(name="Boat", description="A boat", value=10, weight=5), 'quantity': 1},
                                {'item':Item(name="Paddle", description="A paddle", value=10, weight=5), 'quantity': 1},
                                {'item':Item(name="Life Jacket", description="A life jacket", value=10, weight=5), 'quantity': 1},
                            ])
                        )
                    ],
                    inventory=Inventory([
                        {'item':Item(name="Fish", description="A fish", value=1, weight=1), 'quantity': 1},
                        {'item':Item(name="Water", description="Water", value=1, weight=1), 'quantity': 1},
                        {'item':Item(name="Reed", description="Reed", value=1, weight=1), 'quantity': 1},
                    ])
                )
            ],
        )

    def __repr__(self):
        return dumps(self.__dict__, indent=4, cls=q)
    
    def to_json(self):
        return self.__dict__
