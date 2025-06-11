from ..models.game import GameObject, GameWorld

def generate_game(game_data) -> GameWorld:
    game_objects = []
    world_data = {}
    for filename, data in game_data:
        if filename == "world":
            world_data = data
        else:
            game_objects.append(GameObject(**data))

    return GameWorld(game_objects, **world_data)