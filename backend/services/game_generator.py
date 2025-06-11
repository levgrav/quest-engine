from ..models.game import GameObject, GameWorld

def generate_game(game_data) -> GameWorld:
    return GameWorld([GameObject(**data) for _, data in game_data])