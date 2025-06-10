from backend.models.game import Player, GameWorld
from backend.schemas.game import GameResponse
from backend.services.ai import generate_response
import os, pickle

GAME_STATES = {}

world = GameWorld()

def start_game(player_name: str) -> GameResponse:
    player = Player(name=player_name)
    GAME_STATES[player_name] = player
    return GameResponse(
        message=f"Welcome, {player.name}! {world.rooms[player.location]}",
        player_location=player.location
    )

def process_input(player_name: str, input_text: str) -> GameResponse:
    player = GAME_STATES.get(player_name)
    if not player:
        return GameResponse(message="Game not found.", player_location="")
    ai_output = generate_response(input_text, player.location)
    return GameResponse(message=ai_output, player_location=player.location)