import uuid
import os
from .game_generator import generate_game
from .game_loader import load_template
from ..utils.file_ops import pkl_dump, pkl_load

INSTANCE_DIR = "backend/game_data/game_instances"

def list_instances():
    return [f for f in os.listdir(INSTANCE_DIR) if os.path.isdir(os.path.join(INSTANCE_DIR, f))]

def new_game(template_name: str):
    game_data = load_template(template_name)
    session_id = uuid.uuid4()
    game_state = generate_game(game_data)
    print(game_state)
    pkl_dump(INSTANCE_DIR, session_id, game_state)
    return session_id

def load_instance(session_id: str):
    return pkl_load(INSTANCE_DIR, session_id)

def update_game(session_id: str, action: str):
    game_state = pkl_load(INSTANCE_DIR, session_id)
    game_state["log"].append(action)  # stub: real logic goes here
    pkl_dump(INSTANCE_DIR, session_id, game_state)
    return game_state

