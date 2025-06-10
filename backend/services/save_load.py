import os, pickle
from backend.services.game_engine import GAME_STATES

def save_game_state(player_name: str):
    state = GAME_STATES.get(player_name)
    if state:
        with open(f"saves/{player_name}.pkl", "wb") as f:
            pickle.dump(state, f)

def load_game_state(player_name: str):
    try:
        with open(f"saves/{player_name}.pkl", "rb") as f:
            GAME_STATES[player_name] = pickle.load(f)
            state = GAME_STATES[player_name]
            return {
                "message": f"Game loaded. {state.location}",
                "player_location": state.location
            }
    except FileNotFoundError:
        return {
            "message": "No saved game found.",
            "player_location": ""
        }
