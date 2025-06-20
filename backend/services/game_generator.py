from ..models.game import GameObject, GameWorld

def generate_game(game_data) -> GameWorld:
    game_objects = {}
    world_data = {}
    for path, data in game_data.items():
        print(path)
        if path.endswith("world.json"):
            print("world data recognized")
            world_data = data
        else:
            game_objects[path] = GameObject(**data)

    return GameWorld(game_objects, **world_data)